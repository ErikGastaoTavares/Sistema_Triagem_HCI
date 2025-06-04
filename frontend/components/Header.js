import React from 'react';
import Link from 'next/link';

const Header = ({ showAdminButton = true }) => {
  return (
    <header className="header">
      <div className="logo-container">
        <img 
          src="/images/hci_logo.png"
          alt="Logo HCI" 
          className="logo" 
        />
        <h2 className="title">Sistema de Triagem</h2>
      </div>
      
      {showAdminButton && (
        <Link href="/admin">
          <button className="admin-button shadow">
            ÁREA ADMINISTRATIVA
          </button>
        </Link>
      )}
    </header>
  );
};

export default Header;
