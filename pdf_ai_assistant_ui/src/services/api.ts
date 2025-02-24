import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export async function sendDataToServer(data: string) {
	try {
		console.log("📡 Enviando petición a:", `${API_URL}/request_employee`);

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

export async function getHistory(): Promise<{ id: number; prompt: string; created_at: string }[]> {
	try {
		const response = await axios.get(`${API_URL}/history`);
		return response.data; // Debe ser un array
	} catch (error) {
		console.error("❌ Error al obtener historial:", error);
		return []; // Devuelve un array vacío en caso de error
	}
}

export async function downloadPdf(conversationId: number, candidateName: string) {
	const response = await axios.get(`${API_URL}/download/${conversationId}/${candidateName}`, {
		responseType: "blob",
	});

	const blob = new Blob([response.data], { type: "application/pdf" });
	const link = document.createElement("a");
	link.href = window.URL.createObjectURL(blob);
	link.download = `${candidateName}.pdf`;
	link.click();
}
