"use client";

import { useEffect, useRef, useState } from "react";
import { getMessages } from "@/services/api";
import { UiMessage } from "../dto";
import MessageInput from "./MessageInput";
import { useChatStore } from "@/lib/chat-store";
import { sendChatStream } from "@/services/api";
import ReactMarkdown from "react-markdown";

export default function MessagePanel() {
  const { selectedConversationId } = useChatStore();
  const [messages, setMessages] = useState<UiMessage[]>([]);
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
    if(!selectedConversationId) return;
    const data = await getMessages(selectedConversationId);
    setMessages(
      data.map((m) => ({ ...m, isStreaming: false }))
    );
  }

  async function handleSend(content: string) {
    if (!selectedConversationId) return;

    // 1. user message (optimistic)
    const userMsg: UiMessage = {
      id: Date.now(),
      role: "user",
      content,
      conversation_id: selectedConversationId,
    };

    // 2. assistant placeholder
    const assistantId = Date.now() + 1;

    const assistantMsg: UiMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      conversation_id: selectedConversationId,
      isStreaming: true,
    };

    setMessages((prev) => [...prev, userMsg, assistantMsg]);

    // 3. stream
    await sendChatStream(
      selectedConversationId,
      content,
      (token) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? { ...m, content: m.content + token }
              : m
          )
        );
      },
      () => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? { ...m, isStreaming: false }
              : m
          )
        );
      }
    );
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
            
            <b>{m.role}:</b>
            
            {m.role === "assistant" && m.isStreaming && (
              <span>▍</span>
            )}
            
            <ReactMarkdown>
              {m.content}
            </ReactMarkdown>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <MessageInput
        onSend={handleSend}
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