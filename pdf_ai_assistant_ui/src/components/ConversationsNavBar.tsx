import { useEffect, useState } from "react";
import { getHistory } from "../services/api";
import "./ConversationsNavBar.css";

interface Chat {
	id: number;
	prompt: string;
	title: string;
	profile: string;
	created_at: string;
}

interface ConversationsNavBarProps {
	onSelectConversation: (title: string, profile: string, conversationId: number) => void;
}

function ConversationsNavBar({ onSelectConversation }: ConversationsNavBarProps) {
	const [conversations, setConversations] = useState<Chat[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		const fetchChats = async () => {
			try {
				const response = await getHistory();
				setConversations(response);
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
				{conversations.map((chat) => (
					<li
						key={chat.id}
						className="chat-item"
						onClick={() => onSelectConversation(chat.title, chat.profile, chat.id)}
					>
						<div className="chat-title">{chat.title}</div>
						<div className="chat-last-message">
							Última consulta realizada el {new Date(chat.created_at).toLocaleString()}
						</div>
					</li>
				))}
			</ul>
		</div>
	);
}

export default ConversationsNavBar;
