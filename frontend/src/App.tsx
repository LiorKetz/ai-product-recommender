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

  const handleSend = async (text: string) => {
    const userMessage: Message = { role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) throw new Error("API error");

      const data = await response.json();
      const botMessage: Message = { role: "assistant", content: data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const errorMessage: Message = { role: "assistant", content: "Error: could not reach backend" };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };


  const handleNewChat = async () => {
    setMessages([]);  // איפוס ה־state בצד React

    try {
      const response = await fetch("http://127.0.0.1:8000/new_chat", {
        method: "POST",
      });
      if (!response.ok) throw new Error("Failed to reset chat on backend");
    } catch (err) {
      console.error(err);
    }
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

