import React from 'react';

const FormGroup = ({ 
  label, 
  children, 
  htmlFor, 
  error = null,
  className = '' 
}) => {
  return (
    <div className={`form-group ${className}`}>
      {label && (
        <label htmlFor={htmlFor} className="form-label">
          {label}
        </label>
      )}
      {children}
      {error && <p className="text-danger mt-1">{error}</p>}
    </div>
  );
};

export default FormGroup;
