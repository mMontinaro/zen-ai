import { ChatResponse, Conversation, Message } from "@/components/dto";

const API_BASE = "http://localhost:8000";

/** CONVERSATIONS **/
export async function getConversations(): Promise<Conversation[]> {
    const res = await fetch(`${API_BASE}/conversations`);
    if(!res.ok)
        throw new Error("Failted to fetch Conversations");

    return res.json();
}

export async function createConversation(title: string): Promise<Conversation> {
  const res = await fetch(`${API_BASE}/conversations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  if (!res.ok)
    throw new Error("Failed to create conversation");

  return res.json();
}

/** MESSAGES **/
export async function getMessages(conversationId: number): Promise<Message[]> {
  const res = await fetch(
    `${API_BASE}/conversations/${conversationId}/messages`
  );

  if (!res.ok)
    throw new Error("Failed to fetch messages");

  return res.json();
}

/** CHAT **/
export async function sendChatMessage(
  conversationId: number,
  content: string
): Promise<ChatResponse> {
  const res = await fetch(
    `${API_BASE}/chat/${conversationId}`, 
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        role: "user",
        content,
      }),
    }
  );

  if (!res.ok)
    throw new Error("Failed to send message");

  return res.json();
}

export async function sendChatStream(
  conversationId: number,
  content: any,
  onToken: (token: string) => void,
  onDone: () => void
) {
  const res = await fetch(
    `${API_BASE}/chat/${conversationId}/stream`, 
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        role: "user",
        content,
      })
    }
  );

  if (!res.body)
    throw new Error("No stream body");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split("\n");

    for (const line of lines) {
      if (!line.startsWith("data:")) continue;

      const data = line.replace("data: ", "");

      if (data === "[DONE]") {
        onDone();
        return;
      }

      onToken(data);
    }
  }
}