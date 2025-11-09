import React from "react";

interface MessageProps {
  role: "user" | "assistant";
  content: string;
  isRecommendation?: boolean;  // NEW
  feedback?: 'positive' | 'negative' | 'none';  // NEW
  onFeedback?: (feedbackType: 'positive' | 'negative') => void;  // NEW
}

const Message: React.FC<MessageProps> = ({ role, content, isRecommendation, feedback, onFeedback }) => {
  const isUser = role === "user";

  return (
    <div className={`flex mb-4 ${isUser ? "justify-end" : "justify-start"}`}>
      <div className="flex flex-col max-w-[70%]">
        <div
          className={`
            px-4 py-3 rounded-2xl shadow-sm
            ${isUser ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-900"}
          `}
        >
          {content}
        </div>
        
        {/* NEW: Feedback buttons - only for recommendations */}
        {!isUser && isRecommendation && onFeedback && (
          <div className="flex gap-2 mt-2 justify-end">
            <button
              onClick={() => onFeedback('positive')}
              className={`
                p-2 rounded-lg transition-all hover:scale-110
                ${feedback === 'positive' 
                  ? 'bg-green-500 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-green-100'}
              `}
              title="Good recommendation"
            >
              👍
            </button>
            <button
              onClick={() => onFeedback('negative')}
              className={`
                p-2 rounded-lg transition-all hover:scale-110
                ${feedback === 'negative' 
                  ? 'bg-red-500 text-white' 
                  : 'bg-gray-100 text-gray-600 hover:bg-red-100'}
              `}
              title="Bad recommendation"
            >
              👎
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;