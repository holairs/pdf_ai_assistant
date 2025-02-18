import './ChatNavbar.css';

function ChatNavbar() {
  const chats = [
    { id: 1, title: 'Reunión de Proyecto', lastMessage: '¿Listo para la presentación?' },
    { id: 2, title: 'Consulta Rápida', lastMessage: 'Necesito ayuda con el informe.' },
    { id: 3, title: 'Equipo de Desarrollo', lastMessage: 'Actualización del sprint...' },
    { id: 4, title: 'Chat Soporte Técnico', lastMessage: 'Problema resuelto.' },
    { id: 5, title: 'Chat Ventas', lastMessage: 'Cliente interesado en cotización.' },
  ];

  return (
    <div className="chat-navbar">
      <h2>Chats</h2>
      <ul className="chat-list">
        {chats.map((chat) => (
          <li key={chat.id} className="chat-item">
            <div className="chat-title">{chat.title}</div>
            <div className="chat-last-message">{chat.lastMessage}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ChatNavbar;
