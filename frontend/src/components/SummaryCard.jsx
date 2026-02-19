import React from 'react';

const SummaryCard = ({ title, content, type }) => {
  const getCardClass = () => {
    switch (type) {
      case 'extractive': return 'card-extractive';
      case 'abstractive': return 'card-abstractive';
      case 'hybrid': return 'card-hybrid';
      default: return 'bg-white border-gray-200';
    }
  };

  return (
    <div className={`bg-white rounded-lg shadow-sm border overflow-hidden transition-all hover:shadow-md`}>
      <div className={`card-header ${getCardClass()}`}>
        <h3 className="font-semibold text-lg">{title}</h3>
      </div>
      <div className="card-body">
        <p className="text-gray-700 leading-relaxed text-sm">
          {content || "No summary generated."}
        </p>
      </div>
    </div>
  );
};

export default SummaryCard;
