import { useState } from "react";
import "./App.css";
import { sendDataToServer } from "./services/api.js";
import "./components/pixel-canvas.js";
import ReactMarkdown from 'react-markdown';

function App() {
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [responseMessage, setResponseMessage] = useState("");

  const handleSend = async () => {
    setLoading(true);
    setResponseMessage("");

    try {
      const response = await sendDataToServer(inputValue);
      setResponseMessage(`✅ ${response.ai_response}`);
    } catch (error) {
      setResponseMessage("❌ Error al enviar, intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  // Si existe `responseMessage`, agregamos la clase "has-response"
  const mainContainerClass = responseMessage ? "main-container has-response" : "main-container";

  return (
    <div className="wrapper">
      <h1 className="header-title">Employee Finder Assistant</h1>

      {/* Contenedor principal que cambiará de layout cuando haya respuesta */}
      <div className={mainContainerClass}>
        <div className="input-section">
          <textarea
            className="minimal-input"
            placeholder="Escribe aquí..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />

          <div className="card" onClick={handleSend}>
            {/* @ts-ignore */}
            <pixel-canvas
              data-gap="3"
              data-speed="20"
              data-colors="#fef08a, #fde047, #eab308"
            />

            <span className="button-text">
              {loading ? "Enviando..." : "Enviar"}
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
  );
}

export default App;
