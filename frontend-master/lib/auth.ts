import { apiRequest } from "@/lib/api";

export async function login(username: string, password: string) {
    try {
        const response = apiRequest("/auth/login", "POST", { username, password });
        return response;
    } catch(error) {
        throw error;
    }
}

export async function register(username: string, email: string, password: string) {
    try {
        const response = await apiRequest("/auth/register", "POST", { username, email, password });
        return response;
    } catch (error) {
        throw error;
    }
}
