import './Footer.css';

function Footer() {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <p>&copy; {new Date().getFullYear()} EY Employee Finder Assistant. Todos los derechos reservados.</p>
        <div className="footer-links">
          <a href="/politica-privacidad">Política de Privacidad</a>
          <a href="/terminos-condiciones">Términos y Condiciones</a>
          <a href="/contacto">Contacto</a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
