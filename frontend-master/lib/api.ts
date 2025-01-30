const API_BASE_URL = "http://127.0.0.1:5000/api"; 

export async function apiRequest(
  endpoint: string,
  method: string = "GET",
  body?: object
) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    throw new Error(`Error ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

export async function testConnection() {
  return apiRequest("", "GET");
}


// export type JournalEntry = {
//   content: string;
//   mood: string | null;
//   timestamp: string;
//   iaFeedback?: string;
//   feedbackRating?: "like" | "dislike";
// };

// export async function saveEntry(entry: JournalEntry) {
//   const response = await fetch("/api/journal", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(entry),
//   });

//   if (!response.ok) {
//     throw new Error("Error al guardar la entrada");
//   }

//   return response.json();
// }
