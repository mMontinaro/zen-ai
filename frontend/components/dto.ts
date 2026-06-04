export type Conversation = {
    id: number;
    title: string;
}

export type BaseMessage = {
    role: "user" | "assistant";
    content: string;
}

export type Message = BaseMessage & {
    id: number;
    conversation_id: number;
    
}

export type ChatResponse = {
    user_message: Message
    assistant_message: Message
}

export type UiMessage = Message & {
  isStreaming?: boolean;
  isPending?: boolean;
};