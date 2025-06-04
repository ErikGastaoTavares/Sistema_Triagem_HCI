import React from 'react';

const Button = ({ 
  children, 
  onClick, 
  type = 'button', 
  variant = 'primary', 
  className = '', 
  disabled = false,
  fullWidth = false
}) => {
  const buttonClass = `button ${
    variant === 'secondary' ? 'button-secondary' : 
    variant === 'danger' ? 'button-danger' : ''
  } ${fullWidth ? 'w-100' : ''} ${className}`;
  
  return (
    <button
      type={type}
      className={buttonClass}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;
