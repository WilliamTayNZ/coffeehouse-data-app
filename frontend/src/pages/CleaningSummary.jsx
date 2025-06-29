import MainLayout from '../components/MainLayout';
import ContentBox from '../components/ContentBox';

import { useLocation, useNavigate } from 'react-router-dom';

const CleaningSummary = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const summary = location.state?.summary || {};

  const handleProceed = () => {
    navigate('/cleaned-sheets');
  };

  return (
    <MainLayout>
      <ContentBox>
        <h1 className="cleaning-summary-header">🧼 Cleaning Summary</h1>
        {Object.entries(summary).map(([sheetName, sheetSummary]) => (
          <div key={sheetName} className="sheet-summary-block">
            <h2 className="sheet-name">{sheetName}</h2>
            <pre className="cleaning-summary-text">{sheetSummary}</pre>
          </div>
        ))}
      </ContentBox>
    </MainLayout>
  );
};

export default CleaningSummary; 