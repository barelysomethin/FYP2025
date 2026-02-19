import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="flex justify-center items-center" style={{ padding: '2rem 0' }}>
      <div className="animate-spin rounded-full" style={{ height: '3rem', width: '3rem', borderBottom: '2px solid var(--brand-600)', borderRadius: '50%' }}></div>
    </div>
  );
};

export default LoadingSpinner;
