import React, { useState, KeyboardEvent } from "react";
import Button from "../Button";

/**
 * InputBoxProps defines the properties for the InputBox component.
 */
interface InputBoxProps {
  onSend: (message: string) => void;
}

/**
 * InputBox component allows users to type and send messages.
 */
const InputBox: React.FC<InputBoxProps> = ({ onSend }) => {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (text.trim() === "") return;
    onSend(text);
    setText("");
  };

  /**
   * handleKeyPress handles the Enter key press event to send the message.
   */
  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div className="flex space-x-2 flex-1">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Type your message..."
        className="flex-1 px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <Button label="Send" onClick={handleSend} />
    </div>
  );
};

export default InputBox;