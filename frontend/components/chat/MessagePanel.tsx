"use client";

import { useEffect, useRef, useState } from "react";
import { getMessages } from "@/services/api";
import { Message } from "../dto";
import MessageInput from "./MessageInput";
import { useChatStore } from "@/lib/chat-store";

export default function MessagePanel() {
  const { selectedConversationId } = useChatStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    load();
  }, [selectedConversationId]);
  
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  async function load() {
    if(!selectedConversationId){
        return
    }
    const data = await getMessages(selectedConversationId);
    setMessages(data);
  }


  if(!selectedConversationId){
        return (
      <div style={{ padding: 20 }}>
        Select a conversation
      </div>
    );
  } 

  return (
    <div style={styles.container}>
      <div style={styles.messages}>
        {messages.map((m) => (
          <div key={m.id} style={styles.message}>
            <b>{m.role}:</b> {m.content}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <MessageInput
        conversationId={selectedConversationId}
        onMessageSent={(user, assistant) => {
          setMessages((prev) => [
            ...prev,
            user,
            assistant,
          ]);
        }}
      />
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: "flex",
    flexDirection: "column",
    height: "100%",
  },
  messages: {
    flex: 1,
    padding: "12px",
    overflowY: "auto",
  },
  message: {
    marginBottom: "8px",
  },
};