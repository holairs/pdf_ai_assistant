import axios from "axios";

const API_URL = "http://127.0.0.1:8000/request_employee";

export async function sendDataToServer(data: string) {
  try {
    console.log("📡 Enviando petición a:", API_URL);

    const response = await axios.post(
      API_URL,
      JSON.stringify({ prompt: data }),
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    console.log("✅ Respuesta recibida:", response.data);
    return response.data;
  } catch (error: any) {
    console.error("❌ Error al enviar los datos:", error.message || error);
    throw error;
  }
}
