import { useState, useRef, useEffect } from "react";
import "./App.css";
import { downloadPdf, getProcessedProfiles, sendDataToServer } from "./services/api.js";
import "./components/pixel-canvas.js";
import ReactMarkdown from "react-markdown";
import ConversationsNavBar from "./components/ConversationsNavBar.tsx";
import Footer from "./components/Footer.tsx";
import { FaDownload, FaRedo } from "react-icons/fa";

function App() {
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [responseMessage, setResponseMessage] = useState("");
  const [candidates, setCandidates] = useState<{ name: string; conversationId: number }[]>([]);
  const [showInput, setShowInput] = useState(true); // Muestra/oculta el input

  // Referencia al pixel-canvas
  const pixelCanvasRef = useRef(null);

	const handleSelectConversation = async (title: string, profile: string, conversationId: number) => {
			setResponseMessage(`${title} \n ${profile}`);
			console.log("🔍 Buscando perfiles procesados para la conversación:", conversationId);

			try {
					const processedProfiles = await getProcessedProfiles(conversationId);

					console.log("✅ Perfiles obtenidos:", processedProfiles);

					// Transformar los datos al formato correcto
					setCandidates(processedProfiles.map(profile => ({
							name: profile.candidateName, // Ajusta la clave correctamente
							conversationId: conversationId
					})));
			} catch (error) {
					console.error("❌ Error al obtener los perfiles procesados:", error);
					setCandidates([]); // Limpia la lista en caso de error
			}

			setShowInput(false);
	};

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
      // Ocultar el input tras recibir la respuesta
      setShowInput(false);
    } catch (error) {
      setResponseMessage("❌ Error al enviar, intenta de nuevo.");
      setShowInput(true); // Si hay error, volver a mostrar input
    } finally {
      setLoading(false);
    }
  };

  // Maneja la animación del pixel-canvas al terminar de cargar
  useEffect(() => {
    if (!loading && pixelCanvasRef.current) {
      // @ts-ignore
      pixelCanvasRef.current.setForceAnimation(false);
    }
  }, [loading]);

  // Regresar a la pantalla de input
  const handleReset = () => {
    setInputValue("");
    setResponseMessage("");
    setCandidates([]);
    setShowInput(true);
  };

  return (
    <div className="app-container">
			<ConversationsNavBar onSelectConversation={handleSelectConversation} />

      <div className="content-wrapper">
        <div className="wrapper">
          <span>
            <img src="/logo.png" className="logo" alt="Logo" />
          </span>
          <h1 className="header-title">Employee Finder Assistant</h1>

          {/* CONTENEDOR PRINCIPAL -> 400px fijo */}
          <div className="main-container">
            {/* 1) Si showInput es true, mostrar el input */}
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
                  <pixel-canvas
                    ref={pixelCanvasRef}
                    data-gap="3"
                    data-speed="20"
                    data-colors="#fef08a, #fde047, #eab308"
                  />
                  <span className="button-text">{loading ? "Consultando..." : "Enviar"}</span>
                </div>
              </div>
            )}

            {/* 2) Si hay respuesta, mostrar el contenedor de respuesta */}
            {!showInput && responseMessage && (
              <div className="response-section">
                <div className="response">
                  <ReactMarkdown>{responseMessage}</ReactMarkdown>
                </div>

                <div className="reset-section">
                  <button className="reset-btn" onClick={handleReset}>
                    <FaRedo className="icon" /> Nueva Consulta
                  </button>
                </div>

              </div>
            )}
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
