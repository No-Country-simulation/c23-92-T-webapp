// En /lib/api.ts
const API_BASE_URL = "http://localhost:5000/api";

interface ApiResponse {
  success: boolean;
  message?: string;
  data?: any;
  error?: string;
}

export async function handleTokenRefresh(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/token/refresh_token`, {
      method: 'POST',
      credentials: 'include'
    });

    const verifyResponse = await fetch(`${API_BASE_URL}/token/verify_token`, {
      credentials: 'include'
    });

    return verifyResponse.ok;
  } catch (error) {
    console.error('Refresh token failed:', error);
    return false;
  }
}

export async function apiRequest(
  endpoint: string,
  method: string = "GET",
  body?: object,
  timeout: number = 10000
): Promise<ApiResponse> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  const executeRequest = async (): Promise<Response> => {
    return fetch(`${API_BASE_URL}${endpoint}`, {
      method,
      headers: {
        "Content-Type": "application/json",
      },
      body: body ? JSON.stringify(body) : undefined,
      credentials: "include",
      signal: controller.signal
    });
  };

  try {
    let response = await executeRequest();

    if (response.status === 401) {
      const refreshSuccess = await handleTokenRefresh();

      if (refreshSuccess) {
        response = await executeRequest();
      } else {
        window.location.href = '/login';
        return { success: false, message: 'Session expired' };
      }
    }

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `Error ${response.status}`);
    }

    return response.json();
  } catch (error) {
    clearTimeout(timeoutId);

    if (error instanceof Error) {
      if (error.name === "AbortError") {
        return { success: false, message: "Request timed out" };
      }
      return { success: false, message: error.message };
    }

    return { success: false, message: "Unknown error occurred" };
  }
}