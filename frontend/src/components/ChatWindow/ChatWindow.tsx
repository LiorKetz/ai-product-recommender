import React from "react";
import Message from "./Message";
import { ChatWindowProps } from "../../types";


/**
 * ChatWindow component implementation.
 */
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
            isRecommendation={msg.isRecommendation}
            feedback={msg.feedback}
            onFeedback={(feedbackType) => onFeedback(index, feedbackType)}
          />
        ))
      )}
    </div>
  );
};


export default ChatWindow;