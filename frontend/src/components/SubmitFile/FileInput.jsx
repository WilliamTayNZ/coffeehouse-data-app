const FileInput = ({ fileName, onFileChange }) => (
  <div className="file-upload-wrapper">
    <label htmlFor="file" className="file-upload-label">Upload data</label>
    <span id="file-name">{fileName}</span>
    <input
      type="file"
      name="file"
      id="file"
      accept=".xlsx"
      onChange={onFileChange}
      style={{ display: 'none' }}
    />
  </div>
);

export default FileInput; 

// Future: ensure ID uniqueness if multiple FileInput components on same page