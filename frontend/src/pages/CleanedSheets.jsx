//  Not yet push, I created the Modal and handlers for now but realised one problem
// So keep this in mind.

import { useState, useEffect } from 'react';
import MainLayout from '../components/MainLayout';
import ContentBox from '../components/ContentBox';
import React from 'react'; // Needed for React.Fragment
import { previewCleanedSheet, getCleanedSheets } from '../../services/api';

const CleanedSheets = () => {
  const [sheets, setSheets] = useState([]);
  const [previewData, setPreviewData] = useState(null);
  const [previewingId, setPreviewingId] = useState(null);
  const [showSummary, setShowSummary] = useState(false);
  const [cleaningSummary, setCleaningSummary] = useState(null);

  useEffect(() => {
    getCleanedSheets()
      .then(setSheets)
      .catch(() => setSheets([]));
  }, []);

  const handlePreview = async (sheet) => {
    if (previewingId === sheet.id) {
      setPreviewData(null);
      setPreviewingId(null);
      return;
    }
    try {
      const preview = await previewCleanedSheet(sheet.id);
      setPreviewData(preview);
      setPreviewingId(sheet.id);
    } catch (err) {
      setPreviewData({ error: 'Failed to fetch preview.' });
      setPreviewingId(sheet.id);
    }
  };

  const handleViewSummary = async (sheet) => {
    try {
      const res = await fetch(`/api/cleaning_summary/${sheet.id}`);
      const data = await res.json();
      setCleaningSummary(data);
      setShowSummary(true);
    } catch (error) {
      console.error('Failed to fetch cleaning summary:', error);
    }
  };

  const hasAnyInsight = (sheet) =>
    sheet.peak_transaction_times_chart ||
    sheet.most_popular_by_revenue_chart ||
    sheet.most_popular_by_quantity_chart ||
    sheet.highest_revenue_items_chart;

  return (
    <MainLayout>
      <ContentBox>
        <h1>Cleaned Sheets</h1>
        <div className="table-container">
          <table style={{ width: '100%', borderCollapse: 'collapse', tableLayout: 'fixed'}}>
            <thead>
              <tr>
                <th style={{ width: '5%' }}>ID</th>
                <th style={{ width: '7%' }}>Sheet Name</th>
                <th style={{ width: '29%' }}>Original File</th>
                <th style={{ width: '45%' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {sheets.map(sheet => (
                <React.Fragment key={sheet.id}>
                  <tr>
                    <td>{sheet.id}</td>
                    <td>{sheet.sheet_name}</td>
                    <td>{sheet.filename}</td>
                    <td>
                      <div className="button-row">
                        <button
                          className="view-button"
                          onClick={() => handlePreview(sheet)}
                        >
                          {previewingId === sheet.id ? 'Hide Preview' : 'Preview Data'}
                        </button>
                        <button 
                          className="view-button"
                          onClick={() => handleViewSummary(sheet)}
                        >
                          View Cleaning Summary
                        </button>

                        {showSummary && cleaningSummary && (
                          <Modal
                            isOpen={showSummary}
                            onClose={() => setShowSummary(false)}
                          >
                            <h2>Cleaning Summary</h2>
                            <pre>{JSON.stringify(cleaningSummary, null, 2)}</pre>
                          </Modal>
                        )}
                        <button className="view-button" disabled>
                          {hasAnyInsight(sheet) ? 'View Insights' : 'Create Insights'}
                        </button>
                      </div>
                    </td>
                  </tr>
                  {previewingId === sheet.id && previewData && (
                    <tr>
                      <td colSpan={4}>
                        <div style={{ margin: '1rem 0' }}>
                          <h2>Preview Data</h2>
                          {previewData.error ? (
                            <div>{previewData.error}</div>
                          ) : (
                            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                              <thead>
                                <tr>
                                  {previewData.columns?.map(col => (
                                    <th key={col}>{col}</th>
                                  ))}
                                </tr>
                              </thead>
                              <tbody>
                                {previewData.rows?.map((row, idx) => (
                                  <tr key={idx}>
                                    {previewData.columns.map(col => (
                                      <td key={col}>{row[col]}</td>
                                    ))}
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          )}
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      </ContentBox>
    </MainLayout>
  );
};

export default CleanedSheets; 