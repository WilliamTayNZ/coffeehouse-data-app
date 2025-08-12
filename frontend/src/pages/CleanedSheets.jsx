import { useState, useEffect } from 'react';
import React from 'react'; // Needed for React.Fragment

import MainLayout from '../components/MainLayout';
import ContentBox from '../components/ContentBox';
import SummaryModal from '../components/SummaryModal';

import { previewCleanedSheet, getCleanedSheets, getSheetSummary } from '../../services/api';

const CleanedSheets = () => {
  const [sheets, setSheets] = useState([]);
  const [previewData, setPreviewData] = useState(null);
  const [previewingId, setPreviewingId] = useState(null);
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
      const summary = await getSheetSummary(sheet.id);
      setCleaningSummary(summary);
    } catch (error) {
      console.error('Failed to fetch cleaning summary:', error);
    }
  };

  const handleCloseSummary = () => {
    setCleaningSummary(null);
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

                        {cleaningSummary && (<SummaryModal 
                          summary={cleaningSummary}
                          onClose={handleCloseSummary}
                        />)}

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