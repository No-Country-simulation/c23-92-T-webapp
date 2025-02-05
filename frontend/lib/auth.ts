import { apiRequest } from "@/lib/api";

export async function login(username: string, password: string) {
    const response = await apiRequest("/auth/login", "POST", { username, password });

    if (!response.success) {
        throw new Error(response.message ?? "Login failed");
    }

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

export async function logout() {
    const response = await apiRequest("/auth/logout", "POST");

    if (!response.success) {
        throw new Error(response.message ?? "Logout failed");
    }

    return response.data;
}

export async function getProfile() {
    const response = await apiRequest("/auth/get-user", "GET");

    if (!response.success) {
        throw new Error(response.message ?? "Error fetching profile data");
    }

    return response.data;
}

export async function updateProfile(profile: { username: string; email: string; timezone: string }) {
    const response = await apiRequest("/auth/update-user", "PUT", profile);

    if (!response.success) {
        throw new Error(response.message ?? "Error updating profile");
    }

    return response.data;
}

export async function changePassword(currentPassword: string, newPassword: string) {
    const response = await apiRequest("/auth/change-password", "POST", { currentPassword, newPassword });

    if (!response.success) {
        throw new Error(response.message ?? "Error changing password");
    }

    return response.data;
}

export async function deleteAccount() {
    const response = await apiRequest("/auth/delete-account", "DELETE");

    if (!response.success) {
        throw new Error(response.message ?? "Error deleting account");
    }

    return response.data;
}