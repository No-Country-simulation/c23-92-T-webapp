import { io } from "socket.io-client";

const socket = io("https://c23-92-t-webapp-production.up.railway.app", {
    withCredentials: true,
    transports: ['websocket']
});

socket.on("connect", () => {
    console.log("Conectado al servidor de Socket.IO");
});

socket.on("disconnect", () => {
    console.log("Desconectado del servidor de Socket.IO");
});

export interface InteractionResponse {
    success: boolean;
    title?: string;
    response?: string;
    type: "success" | "error"
    error?: string;
}

export default socket;