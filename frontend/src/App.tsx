import React, { useState, useEffect, useRef } from "react";
import ChatWindow from "./components/ChatWindow/ChatWindow";
import InputBox from "./components/ChatWindow/InputBox";
import Button from "./components/Button";
import Dashboard from "./components/Dashboard";
import { MessageProps } from "./types";

// Main chat component
const ChatApp: React.FC = () => {
  const [messages, setMessages] = useState<MessageProps[]>([]);
  const hasMessagesRef = useRef(false);

  // Track if there are messages in the chat
  useEffect(() => {
    hasMessagesRef.current = messages.length > 0;
  }, [messages]);

  // Handle page refresh/close - call new_chat API
  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      // Only call new_chat if there are messages (active conversation)
      if (hasMessagesRef.current) {
        handleNewChat();
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  /**
   * @param text The text message sent by the user
   * Handles sending user message to backend and receiving bot response. 
   * Updates the chat messages state accordingly.
   */
  const handleSend = async (text: string) => {
    const userMessage: MessageProps = { role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) throw new Error("API error");

      const data = await response.json();
      const botMessage: MessageProps = { 
        role: "assistant", 
        content: data.response,
        isRecommendation: data.is_recommendation,
        feedback: 'none'
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const errorMessage: MessageProps = { role: "assistant", content: "Error: could not reach backend" };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  /**
   * @param messageIndex Index of the message to provide feedback on
   * @param feedbackType Type of feedback: 'positive' or 'negative'
   * Handles user feedback on recommendations and sends it to the backend.
   */
  const handleFeedback = async (messageIndex: number, feedbackType: 'positive' | 'negative') => {
    setMessages((prev) =>
      prev.map((msg, idx) =>
        idx === messageIndex ? { ...msg, feedback: feedbackType } : msg
      )
    );

    try {
      await fetch("http://127.0.0.1:8000/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feedback: feedbackType }),
      });
      console.log(`Feedback sent: ${feedbackType}`);
    } catch (err) {
      console.error("Failed to send feedback:", err);
    }
  };

  /**
   * Resets the chat both on frontend and backend.
   */
  const handleNewChat = async () => {
    setMessages([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/new_chat", {
        method: "POST",
      });
      if (!response.ok) throw new Error("Failed to reset chat on backend");
      console.log("Chat reset successfully");
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
        <ChatWindow messages={messages} onFeedback={handleFeedback} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t">
        <InputBox onSend={handleSend} />
      </div>
    </div>
  );
};

// Main App with simple routing
const App: React.FC = () => {
  const [currentPath, setCurrentPath] = useState(window.location.pathname);

  useEffect(() => {
    const handleLocationChange = () => {
      setCurrentPath(window.location.pathname);
    };
    
    window.addEventListener('popstate', handleLocationChange);
    return () => window.removeEventListener('popstate', handleLocationChange);
  }, []);

  if (currentPath === '/dashboard') {
    return <Dashboard />;
  }
  
  return <ChatApp />;
};

export default App;