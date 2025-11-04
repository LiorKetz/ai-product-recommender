import React from "react";

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary";
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({ label, onClick, variant = "primary", disabled = false }) => {
  const baseStyles = "px-4 py-2 rounded-xl font-semibold focus:outline-none focus:ring-2 transition-colors";
  const variantStyles =
    variant === "primary"
      ? "bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-400"
      : "bg-gray-300 text-gray-900 hover:bg-gray-400 focus:ring-gray-400";

  return (
    <button
      className={`${baseStyles} ${variantStyles} ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  );
};

export default Button;