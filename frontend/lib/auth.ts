import { apiRequest } from "@/lib/api";
import { connectSocket, disconnectSocket } from "@/lib/socket";

export async function login(username: string, password: string) {
    const response = await apiRequest("/auth/login", "POST", { username, password });

    if (!response.success) {
        throw new Error(response.message ?? "Login failed");
    }
    
    connectSocket();

    return response.data;
}

export async function register(username: string, email: string, password: string, timezone: string) {
    const response = await apiRequest("/auth/register", "POST", { username, email, password, timezone });

    if (!response.success) {
        throw new Error(response.message ?? "Registration failed");
    }

    return response.data;
}

export const verifyToken = async (): Promise<boolean> => {
    try {
        const response = await apiRequest("/token/verify_token");

        if (!response.success) {
            return false;
        }

        return true;
    } catch (error) {
        return false;
    }
};