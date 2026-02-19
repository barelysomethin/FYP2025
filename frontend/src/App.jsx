import React, { useState } from 'react';
import InputSection from './components/InputSection';
import SummaryCard from './components/SummaryCard';
import LoadingSpinner from './components/LoadingSpinner';
import { summarizeArticle } from './api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSummarize = async (url) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await summarizeArticle(url);
      setResults(data);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header>
        <div className="container flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="logo-box">
              H
            </div>
            <h1 className="font-bold" style={{ fontSize: '1.25rem' }}>Hybrid News Summarizer</h1>
          </div>
          <a
            href="https://github.com/your-repo"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: 'var(--gray-500)', fontSize: '0.875rem', fontWeight: 500, textDecoration: 'none' }}
          >
            v1.0
          </a>
        </div>
      </header>

      {/* Main Content */}
      <main className="container" style={{ flexGrow: 1, padding: '3rem 1rem' }}>
        <div className="flex flex-col gap-8">
          
          <div className="text-center" style={{ marginBottom: '1rem' }}>
             <p style={{ color: 'var(--gray-600)', fontSize: '1.125rem' }}>
                Get extractive, abstractive, and hybrid summaries in seconds using AI.
             </p>
          </div>

          <InputSection onSummarize={handleSummarize} isLoading={isLoading} />

          {error && (
            <div role="alert" style={{ maxWidth: '48rem', margin: '0 auto', width: '100%', backgroundColor: 'var(--red-50)', borderLeft: '4px solid var(--red-500)', color: 'var(--red-700)', padding: '1rem', borderRadius: '0.25rem' }}>
              <p className="font-bold">Error</p>
              <p>{error}</p>
            </div>
          )}

          {isLoading && <LoadingSpinner />}

          {results && (
            <div className="animate-fade-in" style={{ maxWidth: '64rem', margin: '0 auto', width: '100%' }}>
              <div className="flex justify-between items-center" style={{ marginBottom: '1.5rem' }}>
                 <h2 className="font-bold" style={{ fontSize: '1.5rem', color: 'var(--gray-800)' }}>Summarization Results</h2>
                 <div style={{ fontSize: '0.875rem', color: 'var(--gray-500)', backgroundColor: 'var(--white)', padding: '0.25rem 0.75rem', borderRadius: '9999px', border: '1px solid var(--gray-200)' }}>
                    Processing Time: <span style={{ fontFamily: 'monospace', fontWeight: 'bold', color: 'var(--brand-600)' }}>{results.processing_time}s</span>
                 </div>
              </div>
              
              <div className="grid grid-cols-1 md-grid-cols-3 gap-6">
                <SummaryCard
                  title="Extractive (TextRank)"
                  content={results.extractive_summary}
                  type="extractive"
                />
                <SummaryCard
                  title="Abstractive (BART)"
                  content={results.abstractive_summary}
                  type="abstractive"
                />
                <SummaryCard
                  title="Hybrid (Optimized)"
                  content={results.hybrid_summary}
                  type="hybrid"
                />
              </div>
              
              <div className="text-center" style={{ marginTop: '2rem', fontSize: '0.875rem', color: 'var(--gray-400)' }}>
                Original Article Length: {results.article_length} words
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer>
        <div className="container">
          &copy; {new Date().getFullYear()} Hybrid News Summarizer. Built with FastAPI & React.
        </div>
      </footer>
    </div>
  );
}

export default App;
