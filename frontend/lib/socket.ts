import { io, Socket } from "socket.io-client";

const SOCKET_SERVER_URL = "http://localhost:5000"; // Ajusta según tu backend

let socket: Socket | null = null;

export const getSocket = (): Socket => {
  if (!socket) {
    socket = io(SOCKET_SERVER_URL, {
      withCredentials: true,
      autoConnect: false, // No se conecta automáticamente
    });
  }
  return socket;
};

export const connectSocket = () => {
  const socket = getSocket();
  if (!socket.connected) {
    socket.connect();
  }
};

export const disconnectSocket = () => {
  if (socket) {
    socket.disconnect();
  }
};
