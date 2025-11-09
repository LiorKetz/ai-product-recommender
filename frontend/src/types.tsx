
/**
 * MessageProps defines the properties for the Message component.
 */
export interface MessageProps {
  role: "user" | "assistant";
  content: string;
  isRecommendation?: boolean;
  feedback?: 'positive' | 'negative' | 'none';
  onFeedback?: (feedbackType: 'positive' | 'negative') => void;
}

/**
 * ChatWindowProps defines the properties for the ChatWindow component.
 */
export interface ChatWindowProps {
  messages: MessageProps[];
  onFeedback: (messageIndex: number, feedbackType: 'positive' | 'negative') => void;
}