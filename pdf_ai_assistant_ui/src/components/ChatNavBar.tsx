import './ChatNavbar.css';

function ChatNavbar() {
	const chats = [
		{ id: 1, title: 'Perfil de desarrollador flutter', lastMessage: 'John Lennon posee experiencia...' },
		{ id: 2, title: 'Consulta Rápida', lastMessage: 'Estas personas son aptas para...' },
		{ id: 3, title: 'Equipo de Desarrollo', lastMessage: 'Ringo Starr ha trabajado con rust...' },
		{ id: 4, title: 'Perfil de desarrollador cloud', lastMessage: 'Liam posee 12 años de ex...' },
		{ id: 5, title: 'Recomendación de desarrollador CPP', lastMessage: 'Estas personas poseen...' },
	];

	return (
		<div className="chat-navbar">
			<h2>Consultas</h2>
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
