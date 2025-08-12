const SummaryModal = ({ summary, onClose }) => (
  <div className="modal-backdrop">
    <div className="modal">
      <p>{summary}</p>
      <button type="button" onClick={onClose}>Close</button>
    </div>
  </div>
);

export default SummaryModal; 