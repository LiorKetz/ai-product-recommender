import React from "react";
import Message from "./Message";

interface MessageType {
  role: "user" | "assistant";
  content: string;
}

interface ChatWindowProps {
  messages: MessageType[];
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages }) => {
  return (
    <div className="p-4 h-full overflow-y-auto bg-white">
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full text-gray-400">
          Start a new conversation...
        </div>
      ) : (
        messages.map((msg, index) => (
          <Message key={index} role={msg.role} content={msg.content} />
        ))
      )}
    </div>
  );
};

export default ChatWindow;