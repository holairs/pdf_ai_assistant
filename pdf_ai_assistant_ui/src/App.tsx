import { useState } from "react";
import "./App.css";
import { sendDataToServer } from "./services/api.js";
import "./components/pixel-canvas.js";

function App() {

  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [responseMessage, setResponseMessage] = useState("");

  const handleSend = async () => {

    setLoading(true);
    setResponseMessage("");

    try {
      const response = await sendDataToServer(inputValue);
      setResponseMessage(`✅ Enviado: ${response.message}`);
    } catch (error) {
      setResponseMessage("❌ Error al enviar, intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="wrapper">
        <h1 className="header-title">EY Employee Finder Assistant</h1>
        <input
          type="text"
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
            data-colors="#fef08a, 
              #fde047, #eab308"
          >
            {/* @ts-ignore */}
          </pixel-canvas>

          <span className="button-text">{loading ? "Enviando..." : "ENVIAR"}</span>

        </div>
        {responseMessage && <p className="response">{responseMessage}</p>}
      </div>
    </>
  );
}

export default App;
