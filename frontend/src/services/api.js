const API_URL = "http://localhost:8000";

export async function sendMessage(query) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      request_id: crypto.randomUUID(),
      query: query,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail?.message || "Something went wrong"
    );
  }

  return data;
}