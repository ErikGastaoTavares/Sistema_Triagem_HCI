import React from 'react';

const Modal = ({ isOpen, onClose, message }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <div className="modal-content">
          <p>{message}</p>
          <button className="modal-button" onClick={onClose}>
            OK
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;
