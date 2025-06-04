import React from 'react';

const Card = ({ title, children, type = 'default', className = '', footer = null }) => {
  const cardClass = `card ${type === 'success' ? 'card-success' : 
                          type === 'warning' ? 'card-warning' : 
                          type === 'danger' ? 'card-danger' : ''} ${className}`;
  
  return (
    <div className={cardClass}>
      {title && (
        <div className="card-header">
          <h3 className="card-title">{title}</h3>
        </div>
      )}
      
      <div className="card-body">
        {children}
      </div>
      
      {footer && (
        <div className="card-footer">
          {footer}
        </div>
      )}
    </div>
  );
};

export default Card;
