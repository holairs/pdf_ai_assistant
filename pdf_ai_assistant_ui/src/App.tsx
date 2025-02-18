import { useState, useRef, useEffect } from "react";
import "./App.css";
import { sendDataToServer } from "./services/api.js";
import "./components/pixel-canvas.js";
import ReactMarkdown from 'react-markdown';
import ChatNavbar from "./components/ChatNavBar.js";
import Footer from "./components/Footer.js";

function App() {
	const [inputValue, setInputValue] = useState("");
	const [loading, setLoading] = useState(false);
	const [responseMessage, setResponseMessage] = useState("");

	// Referencia al pixel-canvas
	const pixelCanvasRef = useRef(null);

	const handleSend = async () => {
		setLoading(true);
		setResponseMessage("");

		// Forzamos animación mientras "loading"
		if (pixelCanvasRef.current) {
			// @ts-ignore
			pixelCanvasRef.current.setForceAnimation(true);
		}

		try {
			const response = await sendDataToServer(inputValue);
			setResponseMessage(`✅ ${response.ai_response}`);
		} catch (error) {
			setResponseMessage("❌ Error al enviar, intenta de nuevo.");
		} finally {
			setLoading(false);
		}
	};

	// Restablecer animación hover
	useEffect(() => {
		if (!loading && pixelCanvasRef.current) {
			// @ts-ignore
			pixelCanvasRef.current.setForceAnimation(false);
		}
	}, [loading]);

	const mainContainerClass = responseMessage ? "main-container has-response" : "main-container";

	return (
		<div className="app-container">
			<ChatNavbar />

			{/* CONTENIDO PRINCIPAL CENTRADO */}
			<div className="content-wrapper">
				<div className="wrapper">
					<span>
						<img src="/logo.png" className="logo" alt="Logo" />
					</span>
					<h1 className="header-title">Employee Finder Assistant</h1>

					<div className="main-content">
						<div className={mainContainerClass}>
							<div className="input-section">
								<textarea
									className="minimal-input"
									placeholder="Escribe aquí..."
									value={inputValue}
									onChange={(e) => setInputValue(e.target.value)}
								/>

								<div
									className={`card ${loading ? "loading" : ""}`}
									onClick={handleSend}
								>
									{/* @ts-ignore */}
									<pixel-canvas
										ref={pixelCanvasRef}
										data-gap="3"
										data-speed="20"
										data-colors="#fef08a, #fde047, #eab308"
									/>
									<span className="button-text">
										{loading ? "Consultando..." : "Enviar"}
									</span>
								</div>
							</div>

							{responseMessage && (
								<div className="response-section">
									<div className="response">
										<ReactMarkdown>{responseMessage}</ReactMarkdown>
									</div>
								</div>
							)}
						</div>
					</div>
					<Footer />
				</div>
			</div>
		</div>
	);
}

export default App;
