import React from 'react';
import './ChatWidget.css';

const ChatWindow = ({ 
  isOpen, 
  onClose, 
  messages, 
  inputValue, 
  onInputChange, 
  onSendMessage, 
  isLoading 
}) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSendMessage();
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>Textbook Assistant</h3>
        <button onClick={onClose} className="close-button">−</button>
      </div>
      <div className="chat-messages">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`message ${message.sender}-message`}
          >
            <div className="message-content">{message.text}</div>
            {message.sources && message.sources.length > 0 && (
              <div className="message-sources">
                Sources: {message.sources.join(', ')}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message ai-message">
            <div className="message-content">Thinking...</div>
          </div>
        )}
      </div>
      <div className="chat-input-area">
        <textarea
          value={inputValue}
          onChange={(e) => onInputChange(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about the textbook..."
          rows="2"
        />
        <button onClick={onSendMessage} disabled={isLoading}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;