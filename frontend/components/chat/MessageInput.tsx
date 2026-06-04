"use client";

import { useState } from "react";

export default function MessageInput({
  onSend,
}: {
  onSend: (content: string) => Promise<void>;
}) {
  const [value, setValue] = useState("");
  const [loading, setLoading] = useState(false);


  async function send() {
    if(loading) return;
    if (!value.trim()) return;

    setLoading(true);

    try{
      await onSend(value);
      setValue("");
    } finally {
      setLoading(false);
    }

  }

  return (
    <div style={styles.container}>
      <input
        style={styles.input}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            send();
          }
        }}
        placeholder="Type message..."
      />

      <button 
      onClick={send}
      disabled={loading}
      style={styles.button}>
        {loading ? "Awaiting answer..." : "Send"}
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