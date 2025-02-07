import { io } from "socket.io-client";
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:5000/api";


const socket = io(API_BASE_URL, {
    withCredentials: true,
    transports: ['websocket']
});

socket.on("connect", () => {
    console.log("Conectado al servidor de Socket.IO");
});

socket.on("disconnect", () => {
    console.log("Desconectado del servidor de Socket.IO");
});

// src/types/socket.ts
export interface InteractionResponse {
    success: boolean;
    title?: string; // Título opcional
    response?: string; // Respuesta completa (opcional)
    type: "success" | "error"
    error?: string; // Mensaje de error (opcional)
}

export default socket;