const InvalidFileModal = ({ message, onClose }) => (
  <div className="modal-backdrop">
    <div className="modal">
      <p>{message}</p>
      <button type="button" onClick={onClose}>Close</button>
    </div>
  </div>
);

export default InvalidFileModal; 