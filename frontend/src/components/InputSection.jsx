import React, { useState } from 'react';

const InputSection = ({ onSummarize, isLoading }) => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!url) {
      setError('Please enter a URL');
      return;
    }
    // Basic URL validation
    try {
      new URL(url);
    } catch (_) {
      setError('Please enter a valid URL');
      return;
    }
    
    setError('');
    onSummarize(url);
  };

  return (
    <div className="container bg-white rounded-lg shadow-lg" style={{ padding: '2rem', marginBottom: '2.5rem', border: '1px solid var(--gray-100)', maxWidth: '48rem' }}>
      <h2 className="text-2xl font-bold text-center" style={{ color: 'var(--gray-800)', marginBottom: '1.5rem' }}>Summarize News Articles Instantly</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div style={{ position: 'relative' }}>
          <input
            type="url"
            placeholder="Paste article URL here (e.g., https://bbc.com/news/...)"
            className="input-field"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={isLoading}
          />
        </div>
        
        {error && <p style={{ color: 'var(--red-500)', fontSize: '0.875rem' }}>{error}</p>}

        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary"
          style={{ fontSize: '1.125rem', padding: '0.75rem' }}
        >
          {isLoading ? 'Processing...' : 'Summarize Article'}
        </button>
      </form>
    </div>
  );
};

export default InputSection;
