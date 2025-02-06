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

    return response;
}

export async function getProfile() {
    const response = await apiRequest("/auth/get-user", "GET");

    if (!response.success) {
        throw new Error(response.message ?? "Error fetching profile data");
    }

    return response;
}

export async function updateProfile(profile: { username: string; email: string; timezone: string }) {
    try {
        const response = await apiRequest("/auth/update-profile", "PUT", profile);
        if (!response.success) {
            throw new Error(response.message ?? "Error updating profile");
        }
        return response;
    } catch (error) {
        console.error("Error updating profile:", error);
        throw error;
    }
}

export async function changePassword(data: { current_password: string; new_password: string }) {
    if (!data.current_password || !data.new_password) {
        throw new Error("Both current password and new password are required");
    }

    try {
        const response = await apiRequest("/auth/update-password", "PUT", {
            current_password: data.current_password,
            new_password: data.new_password,
        });

        if (!response.success) {
            throw new Error(response.message ?? "Error changing password");
        }
        return response;
    } catch (error) {
        console.error("Error changing password:", error);
        throw error;
    }
}

export async function deleteAccount() {
    const response = await apiRequest("/auth/delete-account", "DELETE");

    if (!response.success) {
        throw new Error(response.message ?? "Error deleting account");
    }

    return response;
}