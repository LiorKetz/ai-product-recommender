import React from "react";

interface MessageProps {
  role: "user" | "assistant";
  content: string;
}

const Message: React.FC<MessageProps> = ({ role, content }) => {
  const isUser = role === "user";

  return (
    <div className={`flex mb-4 ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`
          max-w-[70%] px-4 py-3 rounded-2xl shadow-sm
          ${isUser ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-900"}
        `}
      >
        {content}
      </div>
    </div>
  );
};

export default Message;