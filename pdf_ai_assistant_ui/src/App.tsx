import { useState, useRef, useEffect } from "react";
import "./App.css";
import { downloadPdf, sendDataToServer } from "./services/api.js";
import "./components/pixel-canvas.js";
import ReactMarkdown from "react-markdown";
import ConversationsNavBar from "./components/ConversationsNavBar.tsx";
import Footer from "./components/Footer.tsx";
import { FaDownload, FaRedo } from "react-icons/fa"; // Importa íconos

function App() {
	const [inputValue, setInputValue] = useState("");
	const [loading, setLoading] = useState(false);
	const [responseMessage, setResponseMessage] = useState("");
	const [candidates, setCandidates] = useState<{ name: string; conversationId: number }[]>([]);
	const [showInput, setShowInput] = useState(true); // Estado para ocultar el input después del request

	// Referencia al pixel-canvas
	const pixelCanvasRef = useRef(null);

	const handleSend = async () => {
		setLoading(true);
		setResponseMessage("");
		setCandidates([]);


		// Forzar animación mientras "loading"
		if (pixelCanvasRef.current) {
			// @ts-ignore
			pixelCanvasRef.current.setForceAnimation(true);
		}

		try {
			const response = await sendDataToServer(inputValue);

			// Actualizar respuesta principal
			setResponseMessage(`${response.title} \n ${response.profile}`);

			// Extraer candidatos si existen en la respuesta
			if (response.candidates) {
				setCandidates(response.candidates);
			}
		} catch (error) {
			setResponseMessage("❌ Error al enviar, intenta de nuevo.");
			setShowInput(true); // Si hay error, volver a mostrar el input
		} finally {
			setLoading(false);
			setShowInput(false);

		}
	};

	// Restablecer animación hover
	useEffect(() => {
		if (!loading && pixelCanvasRef.current) {
			// @ts-ignore
			pixelCanvasRef.current.setForceAnimation(false);
		}
	}, [loading]);

	// Restablecer la UI para hacer una nueva consulta
	const handleReset = () => {
		setInputValue("");
		setResponseMessage("");
		setCandidates([]);
		setShowInput(true);
	};

	return (
		<div className="app-container">
			<ConversationsNavBar />

			{/* CONTENIDO PRINCIPAL CENTRADO */}
			<div className="content-wrapper">
				<div className="wrapper">
					<span>
						<img src="/logo.png" className="logo" alt="Logo" />
					</span>
					<h1 className="header-title">Employee Finder Assistant</h1>

					<div className={`main-container ${responseMessage ? "has-response" : ""}`}>
						{/* Sección de input (desaparece si showInput es false) */}
						{showInput && (
							<div className="input-section">
								<textarea
									className="minimal-input"
									placeholder="Escribe aquí..."
									value={inputValue}
									onChange={(e) => setInputValue(e.target.value)}
								/>

								<div className={`card ${loading ? "loading" : ""}`} onClick={handleSend}>
									{/* @ts-ignore */}
									<pixel-canvas ref={pixelCanvasRef} data-gap="3" data-speed="20" data-colors="#fef08a, #fde047, #eab308" />
									<span className="button-text">{loading ? "Consultando..." : "Enviar"}</span>
								</div>
							</div>
						)}

						{/* Sección de respuesta */}
						{responseMessage && (
							<div className="response-section">
								<div className="response">
									<ReactMarkdown>{responseMessage}</ReactMarkdown>
								</div>

								{/* 🔹 Botón de Nueva Consulta */}
								<div className="reset-section">
									<button className="reset-btn" onClick={handleReset}>
										<FaRedo className="icon" /> Continuar con la consulta
									</button>
								</div>

							</div>
						)}
						{/* 🔹 Sección de Descarga */}
						{candidates.length > 0 && (
							<div className="download-buttons">
							<h3>Descargar Perfiles</h3>
							{candidates.map((candidate, index) => (
								<div key={index} className="download-item">
								<button
								className="download-btn"
								onClick={() => downloadPdf(candidate.conversationId, candidate.name)}
								>
								<FaDownload className="icon" />
								</button>
								<span className="candidate-name">{candidate.name}</span>
								</div>
							))}
							</div>
						)}
					</div>
					<Footer />
				</div>
			</div>
		</div>
	);
}

export default App;
