import React, { useState } from 'react';

const PersonalizeButton = ({ content, onContentChange }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedBackground, setSelectedBackground] = useState('general');

  const handlePersonalize = () => {
    // In a real implementation, this would call the backend API to personalize content
    let personalizedContent = content;
    
    switch(selectedBackground) {
      case 'python-expert':
        personalizedContent = `**For Python Experts:** ${content}`;
        break;
      case 'beginner':
        personalizedContent = `**Simplified for Beginners:** ${content}`;
        break;
      case 'hardware-focused':
        personalizedContent = `**Hardware Perspective:** ${content}`;
        break;
      case 'software-focused':
        personalizedContent = `**Software Perspective:** ${content}`;
        break;
      default:
        break;
    }
    
    onContentChange(personalizedContent);
    setIsModalOpen(false);
  };

  return (
    <div className="personalize-button">
      <button
        onClick={() => setIsModalOpen(true)}
        className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50"
      >
        Personalize Content
      </button>

      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-96">
            <h3 className="text-lg font-semibold mb-4">Select Your Background</h3>
            
            <div className="space-y-3 mb-6">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="background"
                  value="general"
                  checked={selectedBackground === 'general'}
                  onChange={(e) => setSelectedBackground(e.target.value)}
                  className="mr-2"
                />
                General (Default)
              </label>
              
              <label className="flex items-center">
                <input
                  type="radio"
                  name="background"
                  value="python-expert"
                  checked={selectedBackground === 'python-expert'}
                  onChange={(e) => setSelectedBackground(e.target.value)}
                  className="mr-2"
                />
                Python Expert
              </label>
              
              <label className="flex items-center">
                <input
                  type="radio"
                  name="background"
                  value="beginner"
                  checked={selectedBackground === 'beginner'}
                  onChange={(e) => setSelectedBackground(e.target.value)}
                  className="mr-2"
                />
                Complete Beginner
              </label>
              
              <label className="flex items-center">
                <input
                  type="radio"
                  name="background"
                  value="hardware-focused"
                  checked={selectedBackground === 'hardware-focused'}
                  onChange={(e) => setSelectedBackground(e.target.value)}
                  className="mr-2"
                />
                Hardware Focused
              </label>
              
              <label className="flex items-center">
                <input
                  type="radio"
                  name="background"
                  value="software-focused"
                  checked={selectedBackground === 'software-focused'}
                  onChange={(e) => setSelectedBackground(e.target.value)}
                  className="mr-2"
                />
                Software Focused
              </label>
            </div>
            
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setIsModalOpen(false)}
                className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100 focus:outline-none"
              >
                Cancel
              </button>
              <button
                onClick={handlePersonalize}
                className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 focus:outline-none"
              >
                Apply Personalization
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PersonalizeButton;