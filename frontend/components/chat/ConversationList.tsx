"use client"

import { useEffect, useState } from "react";
import { getConversations, createConversation } from "@/services/api";
import { Conversation } from "../dto";
import { useChatStore } from "@/lib/chat-store";

export default function ConversationList() {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const { selectedConversationId, setSelectedConversationId } = useChatStore();

    async function load(){
        const data = await getConversations();
        setConversations(data);
        if(!selectedConversationId && data.length > 0){
            setSelectedConversationId(data[0].id);
        }
    }

    async function newChat(){
        const title = "New Chat";
        const conversation = await createConversation(title);
        await load();
        setSelectedConversationId(conversation.id);
    }

    useEffect(() => {
        load();
    }, []);

    return (
        <div>
            <div>
                <h3 style={styles.header}>Conversations</h3>
                <button onClick={newChat}>+</button>
            </div>
            
            {conversations.map((c) => (
                <div 
                    key={c.id}
                    onClick={() => setSelectedConversationId(c.id)}
                    style={{
                    ...styles.item,
                    background:
                    selectedConversationId === c.id
                        ? "#e5e5e5"
                        : "transparent",
                }}>
                    {c.title}
                </div>
            ))}
        </div>
    );
    

    
}

const styles: Record<string, React.CSSProperties> = {
    header: {
        display: "flex",
        justifyContent: "space-between",
        marginBottom: 12,
    },
    item: {
        padding: "8px",
        borderRadius: "6px",
        cursor: "pointer",
        },
};
