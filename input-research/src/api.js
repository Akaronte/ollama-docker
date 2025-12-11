const ENDPOINT_URL = "/research"; // Nginx hace proxy a http://deep-research-agent:8000/research

export async function postText(text) {
  const payload = { query: text, depth: 3 };
  console.log("[REQUEST]", ENDPOINT_URL, payload);

  const response = await fetch(ENDPOINT_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  console.log("[RESPONSE] status:", response.status, response.statusText);

  const data = await response.json();
  console.log("[RESPONSE] body:", data);

  if (!response.ok) {
    const message = `Error HTTP ${response.status}`;
    throw new Error(message);
  }

  return data;
}
