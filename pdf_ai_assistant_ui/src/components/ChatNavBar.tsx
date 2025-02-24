import { useEffect, useState } from "react";
import { getHistory } from "../services/api";
import "./ChatNavbar.css";

interface Chat {
	id: number;
	prompt: string;
	created_at: string;
}

function ChatNavbar() {
	const [chats, setChats] = useState<Chat[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		const fetchChats = async () => {
			try {
				const response = await getHistory();
				setChats(response);
			} catch (err) {
				console.error("❌ Error al obtener el historial:", err);
				setError("Error al cargar conversaciones.");
			} finally {
				setLoading(false);
			}
		};

		fetchChats();
	}, []);

	return (
		<div className="chat-navbar">
			<h2>Consultas</h2>

			{loading && <p>Cargando...</p>}
			{error && <p className="error">{error}</p>}

			<ul className="chat-list">
				{chats.map((chat) => (
					<li key={chat.id} className="chat-item">
						<div className="chat-title">{chat.prompt}</div>
						<div className="chat-last-message">Última consulta realizada el {new Date(chat.created_at).toLocaleString()}</div>
					</li>
				))}
			</ul>
		</div>
	);
}

export default ChatNavbar;
