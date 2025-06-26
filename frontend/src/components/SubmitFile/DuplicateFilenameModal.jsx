import React from 'react';

const DuplicateFilenameModal = ({ filename, onReplace, onCancel }) => (
    <div className="modal-backdrop">
      <div className="modal">
        <p>
          <b>{filename}</b> already exists. <br/>
          Do you want to replace it?
        </p>
        <div className="modal-actions">
          <button type="button" onClick={onReplace}>Replace</button>
          <button type="button" onClick={onCancel}>Cancel</button>
        </div>
      </div>
    </div>
    );

export default DuplicateFilenameModal;