import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow/ChatWindow";
import InputBox from "./components/ChatWindow/InputBox";
import Button from "./components/Button";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSend = (text: string) => {
    const userMessage: Message = { role: "user", content: text };
    const fakeResponse: Message = { role: "assistant", content: "Automated response from bot" };

    setMessages((prev) => [...prev, userMessage, fakeResponse]);
  };

  const handleNewChat = () => {
    setMessages([]);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white border-b p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">Chat Bot</h1>
        <Button label="New Chat" variant="secondary" onClick={handleNewChat} />
      </div>

      {/* Chat Window */}
      <div className="flex-1 overflow-hidden">
        <ChatWindow messages={messages} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t">
        <InputBox onSend={handleSend} />
      </div>
    </div>
  );
};

export default App;

