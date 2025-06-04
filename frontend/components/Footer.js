import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <img 
        src="/images/hci_logo.png"
        alt="Logo HCI" 
        className="footer-logo" 
      />
      <p className="mb-1"><strong>Sistema de Triagem - Hospital de Clínicas Ijuí</strong></p>
      <p className="mb-1">Desenvolvido conforme o Protocolo de Manchester</p>
      <p className="mb-1">© {new Date().getFullYear()} - Todos os direitos reservados</p>
    </footer>
  );
};

export default Footer;
