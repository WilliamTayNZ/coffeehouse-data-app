const ExistingFilesList = ({ existingFiles, currentlyPreviewed, currentlySelected, onPreview, onSelect }) => (
  <div id="existing-files-section" style={{ display: 'block' }}>
    <h2>Existing Files</h2>
    <p style={{ fontFamily: 'Poppins, sans-serif' }}>
      Previously uploaded <b>uncleaned</b> files. <br/><br/>
      <b>Note:</b> Clicking 'Select' will override any uploaded file.
    </p>
    <ul id="existing-files-list">
      {existingFiles.length === 0 ? (
        <li>No existing files found.</li>
      ) : (
        existingFiles.map((filename) => (
          <li key={filename}>
            <span className="file-name">{filename}</span>
            <div className="file-actions">
              <button
                type="button"
                className={`preview-button${currentlyPreviewed === filename ? ' previewing' : ''}`}
                onClick={() => onPreview(filename)}
              >
                Preview
              </button>
              <button
                type="button"
                className={`select-button${currentlySelected === filename ? ' selected' : ''}`}
                onClick={() => onSelect(filename)}
              >
                Select
              </button>
            </div>
          </li>
        ))
      )}
    </ul>
  </div>
  );
  
export default ExistingFilesList; 