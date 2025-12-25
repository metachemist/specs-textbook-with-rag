import React from 'react';
import ChatWidget from '../components/ChatWidget/ChatWidget';

// This component wraps the entire application
// It's loaded on every page of the Docusaurus site
export default function Root({ children }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}