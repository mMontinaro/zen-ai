"use client";

import { useState } from "react";
import { sendChatMessage } from "@/services/api";

export default function MessageInput({
  conversationId,
  onMessageSent,
}: {
  conversationId: number;
  onMessageSent: () => void;
}) {
  const [value, setValue] = useState("");

  async function send() {
    if (!value.trim()) return;

    await sendChatMessage(conversationId, value);

    setValue("");
    onMessageSent();
  }

  return (
    <div style={styles.container}>
      <input
        style={styles.input}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Type message..."
      />

      <button onClick={send} style={styles.button}>
        Send
      </button>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: "flex",
    gap: "8px",
    padding: "12px",
    borderTop: "1px solid #ddd",
  },
  input: {
    flex: 1,
    padding: "10px",
  },
  button: {
    padding: "10px 16px",
  },
};