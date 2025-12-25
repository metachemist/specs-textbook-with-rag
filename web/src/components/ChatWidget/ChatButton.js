import React from 'react';
import './ChatWidget.css';

const ChatButton = ({ onClick }) => {
  return (
    <button className="chat-toggle-button" onClick={onClick}>
      💬 Chat
    </button>
  );
};

export default ChatButton;