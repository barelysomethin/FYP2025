import os
import requests
import networkx as nx
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from newspaper import Article
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn
from dotenv import load_dotenv
import logging

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Environment Variables
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
HF_API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

# Initialize NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Initialize FastAPI
app = FastAPI(title="Hybrid News Summarizer")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class SummaryRequest(BaseModel):
    url: str

class SummaryResponse(BaseModel):
    extractive_summary: str
    abstractive_summary: str
    hybrid_summary: str
    article_length: int
    processing_time: float

# --- Helper Functions ---

def extract_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logger.error(f"Error extracting article: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract article from URL.")

def extractive_summary(text, num_sentences=5):
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # Cosine Similarity Matrix
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # PageRank
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    
    # Sort by score
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    
    # Select top N and sort by original order
    selected_sentences = [s for _, s in ranked_sentences[:num_sentences]]
    
    # Reorder sentences as they appear in the original text
    # Finding indices of selected sentences to sort them
    
    # Quick way to reorder: 
    # Just return the top ranked ones for now, or match/sort.
    # Better: keep original index during ranking.
    
    ranked_with_index = sorted(((scores[i], i, s) for i, s in enumerate(sentences)), reverse=True)[:num_sentences]
    ranked_with_index.sort(key=lambda x: x[1]) # Sort by original index
    
    return " ".join([s for _, _, s in ranked_with_index])

def query_hf_api(payload):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    logger.info(f"HF API Status: {response.status_code}")
    logger.info(f"HF API Response: {response.text}")
    try:
        return response.json()
    except ValueError:
        logger.error(f"Failed to decode JSON from HF API. Status: {response.status_code}, Response: {response.text}")
        return {"error": f"HF API Error (Status {response.status_code}): {response.text}"}

def abstractive_summary(text):
    if not HF_API_KEY:
        return "Error: Hugging Face API Key not set."
    
    # Chunking if text is too long (BART limit is ~1024 tokens)
    # Simple truncation for V1 (first 3000 chars roughly)
    truncated_text = text[:3000] 
    
    payload = {
        "inputs": truncated_text,
        "parameters": {"max_length": 150, "min_length": 40, "do_sample": False}
    }
    
    try:
        output = query_hf_api(payload)
        if isinstance(output, list) and 'summary_text' in output[0]:
            return output[0]['summary_text']
        elif 'error' in output:
             return f"API Error: {output['error']}"
        return "Failed to generate abstractive summary."
    except Exception as e:
        logger.error(f"HF API Error: {e}")
        return "Error calling Abstractive API."

def hybrid_summary(text):
    # Step 1: Extractive (reduce to important parts)
    # Reduce to ~10-15 sentences to capture key info
    extractive_part = extractive_summary(text, num_sentences=10)
    
    # Step 2: Abstractive on the reduced text
    return abstractive_summary(extractive_part)

# --- Routes ---

@app.post("/summarize", response_model=SummaryResponse)
async def summarize(request: SummaryRequest):
    import time
    start_time = time.time()
    
    article_text = extract_article(request.url)
    
    # Run summaries
    # In a real app, maybe run these in parallel using asyncio
    ext_sum = extractive_summary(article_text)
    abs_sum = abstractive_summary(article_text)
    hyb_sum = hybrid_summary(article_text)
    
    end_time = time.time()
    
    return SummaryResponse(
        extractive_summary=ext_sum,
        abstractive_summary=abs_sum,
        hybrid_summary=hyb_sum,
        article_length=len(article_text.split()),
        processing_time=round(end_time - start_time, 2)
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
