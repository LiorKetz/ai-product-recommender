import React from "react";
import Message from "./Message";

interface MessageType {
  role: "user" | "assistant";
  content: string;
  isRecommendation?: boolean;  // NEW
  feedback?: 'positive' | 'negative' | 'none';  // NEW
}

interface ChatWindowProps {
  messages: MessageType[];
  onFeedback: (messageIndex: number, feedbackType: 'positive' | 'negative') => void;  // NEW
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages, onFeedback }) => {
  return (
    <div className="p-4 h-full overflow-y-auto bg-white">
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full text-gray-400">
          Start a new conversation...
        </div>
      ) : (
        messages.map((msg, index) => (
          <Message 
            key={index} 
            role={msg.role} 
            content={msg.content}
            isRecommendation={msg.isRecommendation}  // NEW
            feedback={msg.feedback}  // NEW
            onFeedback={(feedbackType) => onFeedback(index, feedbackType)}  // NEW
          />
        ))
      )}
    </div>
  );
};

export default ChatWindow;