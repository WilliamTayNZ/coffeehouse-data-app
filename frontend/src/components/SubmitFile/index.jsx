import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../../components-styles/SubmitFile.css';

import FileInput from './FileInput';
import DuplicateFilenameModal from './DuplicateFilenameModal';
import InvalidFileModal from './InvalidFileModal';
import ExistingFilesList from './ExistingFilesList';
import FilePreviewTable from './FilePreviewTable';

import { loadExistingFiles, previewUncleanedFile, uploadFile, cleanFile } from '../../services/api';

const SubmitFile = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const [pendingUploadFile, setPendingUploadFile] = useState(null);
  const [showDuplicateModal, setShowDuplicateModal] = useState(false);
  const [invalidFileMessage, setInvalidFileMessage] = useState('');

  const [existingFiles, setExistingFiles] = useState([]);
  const [showExisting, setShowExisting] = useState(false);

  const [previewData, setPreviewData] = useState(null);
  const [currentlyPreviewed, setCurrentlyPreviewed] = useState(null);

  const navigate = useNavigate();
  

  const displayFileName = selectedFile
  ? (typeof selectedFile === 'string' ? selectedFile : selectedFile.name)
  : 'No file chosen'; 

  
  const refreshExistingFiles = async () => {
    try {
      const data = await loadExistingFiles();
      setExistingFiles(data.files);
    } catch (err) {
      setExistingFiles([]);
    }
  };

  useEffect(() => {
    refreshExistingFiles();
  }, []);


  const doUpload = async (file) => {
    try {
      await uploadFile(file);
      setSelectedFile(file.name);
      await refreshExistingFiles();
      const name = file.name;
      if (currentlyPreviewed === name) {
        await handlePreview(name);
      }
      return true;
    } catch (err) {
      setInvalidFileMessage(err.message || 'File upload failed.');
      return false;
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const exists = existingFiles.includes(file.name);
    if (exists) {
      setPendingUploadFile(file);
      setShowDuplicateModal(true);
      e.target.value = "";
      return;
    }
    // Upload new file
    await doUpload(file);
    e.target.value = "";
  };

  const handleDuplicateModalReplace = async () => {
    if (pendingUploadFile) {
      await doUpload(pendingUploadFile);
    }
    setShowDuplicateModal(false);
    setPendingUploadFile(null);
  };
  
  const handleDuplicateModalCancel = () => {
    setShowDuplicateModal(false);
    setPendingUploadFile(null);
  };
  
  const handleInvalidFileClose = () => {
    setInvalidFileMessage('');
  };
  
  const handleViewExistingFiles = () => {
    setShowExisting((prev) => !prev);
    setPreviewData(null);
    setCurrentlyPreviewed(null);
  };

  const handlePreview = async (filename) => {
    if (currentlyPreviewed === filename) {
      setPreviewData(null);
      setCurrentlyPreviewed(null);
      return;
    }
    try {
      const preview = await previewUncleanedFile(filename);
      setPreviewData(preview);
      setCurrentlyPreviewed(filename);
    } catch (err) {
      setPreviewData("Error: failed to preview data");
    }
  };


  // Select a file
  const handleSelectExisting = (filename) => {
    if (selectedFile === filename) {
      setSelectedFile(null);
    } else {
      setSelectedFile(filename); // string
    }
  };

  // Handle form submit (clean data)
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await cleanFile(selectedFile);
      const filename = typeof selectedFile === 'string' ? selectedFile : selectedFile.name;
      navigate(`/${encodeURIComponent(filename)}/cleaning-summary`, { state: { summary: result.summary } });
    } catch (err) {
      setInvalidFileMessage(err.message || 'Failed to clean file.');
    }
  };

  return (
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <h1>Upload Sales Data</h1>
        <label htmlFor="file">Upload your franchise's sales data (.xlsx):</label><br />
        <FileInput
          fileName={displayFileName}
          onFileChange={handleFileUpload}
        />

        {showDuplicateModal && (
          <DuplicateFilenameModal
          filename={pendingUploadFile?.name}
          onReplace={handleDuplicateModalReplace}
          onCancel={handleDuplicateModalCancel}
          />
          )}

        {invalidFileMessage && (
          <InvalidFileModal
            message={invalidFileMessage}
            onClose={handleInvalidFileClose}
          />
        )}

        {/* View Existing Files Button */}
        <button 
        type="button" 
        className={`view-button${showExisting ? ' active' : ''}`} 
        onClick={handleViewExistingFiles}>
        View existing files
        </button>

        {/* Existing Files Section */}
        {showExisting && (
          <ExistingFilesList
            existingFiles={existingFiles}
            currentlyPreviewed={currentlyPreviewed}
            currentlySelected={selectedFile}
            onPreview={handlePreview}
            onSelect={handleSelectExisting}
          />
        )}

        {/* File Preview Section */}
        <FilePreviewTable previewData={previewData} />

        {/* Clean Data Button */}
        <button type="submit" id="clean-button" disabled={!selectedFile}>
          Clean data
        </button>

      </form>
  );
};

export default SubmitFile; 