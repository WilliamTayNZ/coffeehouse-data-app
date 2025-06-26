import React from 'react';
import { useNavigate } from 'react-router-dom';

const CleaningSummary = ({ summary }) => {
  const navigate = useNavigate();

  const handleProceed = () => {
    navigate('/cleaned-sheets');
  };

  return (
    <div style={{ padding: '2rem', maxWidth: 600, margin: '0 auto', textAlign: 'center' }}>
      <h1>🧼 Cleaning Summary</h1>
      <pre style={{ background: '#f6f6f6', padding: '1rem', borderRadius: '8px', textAlign: 'left' }}>{summary}</pre>
      <button onClick={handleProceed} style={{ marginTop: '2rem', padding: '0.75rem 1.5rem', fontSize: '1rem' }}>
        ➡️ View Cleaned Sheets
      </button>
    </div>
  );
};

export default CleaningSummary; 