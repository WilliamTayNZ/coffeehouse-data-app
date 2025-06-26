const FilePreviewTable = ({ previewData }) => {
  if (!previewData) return null;
  
  return (
    <div id="file-preview">
      <table>
        <thead>
          <tr>
            {previewData.columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {previewData.rows.map((row, index) => (
            <tr key={index}>
              {previewData.columns.map((col) => (
                <td key={col}>{row[col] ?? ''}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FilePreviewTable; 