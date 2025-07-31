import { useState, useEffect } from 'react';
import MainLayout from '../components/MainLayout';
import ContentBox from '../components/ContentBox';
import React from 'react'; // Added missing import for React

const API_URL = '/api/cleaned_sheets';

const CleanedSheets = () => {
  const [sheets, setSheets] = useState([]);
  const [previewData, setPreviewData] = useState(null);
  const [previewingId, setPreviewingId] = useState(null);

  useEffect(() => {
    fetch(API_URL)
      .then(res => res.json())
      .then(setSheets)
      .catch(() => setSheets([]));
  }, []);

  /* handlePreview: Could be further optimized with caching if users preview the same sheet repeatedly, 
  but this is not necessary for most apps. */
  const handlePreview = async (sheet) => {
    if (previewingId === sheet.id) {
      setPreviewData(null);
      setPreviewingId(null);
      return;
    }
    try {
      const res = await fetch(`/api/preview_file/${encodeURIComponent(sheet.filename)}`);
      const data = await res.json();
      setPreviewData(data);
      setPreviewingId(sheet.id);
    } catch {
      setPreviewData({ error: 'Failed to fetch preview.' });
      setPreviewingId(sheet.id);
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
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Sheet Name</th>
                <th>Original File</th>
                <th>Actions</th>
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
                        <button className="view-button" disabled>
                          View Cleaning Summary
                        </button>
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