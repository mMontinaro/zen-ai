export type Conversation = {
    id: number;
    title: string;
}

export type Message = {
    id: number;
    conversation_id: number;
    role: "user" | "assistant";
    content: string;
}