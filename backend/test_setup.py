import os
import sys

try:
    import fastapi
    import newspaper
    import nltk
    import networkx
    import requests
    import dotenv
    print("Imports successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    print("NLTK data found.")
except LookupError:
    print("NLTK data not found. Automatic download should happen in main.py.")

print("Backend setup check passed.")
