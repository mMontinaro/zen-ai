import { create } from "zustand";

type ChatStore = {
  selectedConversationId: number | null;
  setSelectedConversationId: (id: number) => void;
};

export const useChatStore = create<ChatStore>((set) => ({
  selectedConversationId: null,

  setSelectedConversationId: (id) =>
    set({
      selectedConversationId: id,
    }),
}));