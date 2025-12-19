import React, { useState } from 'react';

const TranslateButton = ({ content, onContentChange }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('urdu');
  const [isTranslating, setIsTranslating] = useState(false);

  const handleTranslate = () => {
    setIsTranslating(true);
    
    // In a real implementation, this would call a translation API
    // For now, we'll simulate the translation process
    setTimeout(() => {
      let translatedContent = content;
      
      if (selectedLanguage === 'urdu') {
        // This is just a placeholder - in reality, we'd call an API to translate to Urdu
        translatedContent = `**This content has been translated to Urdu:**\n\n${content}`;
      }
      
      onContentChange(translatedContent);
      setIsTranslating(false);
      setIsModalOpen(false);
    }, 1500); // Simulate API call delay
  };

  return (
    <div className="translate-button">
      <button
        onClick={() => setIsModalOpen(true)}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
      >
        Translate
      </button>

      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-96">
            <h3 className="text-lg font-semibold mb-4">Select Language</h3>
            
            <div className="space-y-3 mb-6">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="language"
                  value="urdu"
                  checked={selectedLanguage === 'urdu'}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="mr-2"
                />
                Urdu
              </label>
              
              <label className="flex items-center">
                <input
                  type="radio"
                  name="language"
                  value="spanish"
                  checked={selectedLanguage === 'spanish'}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="mr-2"
                />
                Spanish
              </label>
              
              <label className="flex items-center">
                <input
                  type="radio"
                  name="language"
                  value="french"
                  checked={selectedLanguage === 'french'}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="mr-2"
                />
                French
              </label>
            </div>
            
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setIsModalOpen(false)}
                className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100 focus:outline-none"
                disabled={isTranslating}
              >
                Cancel
              </button>
              <button
                onClick={handleTranslate}
                disabled={isTranslating}
                className={`px-4 py-2 rounded focus:outline-none ${
                  isTranslating 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-green-600 hover:bg-green-700 text-white'
                }`}
              >
                {isTranslating ? 'Translating...' : 'Translate'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TranslateButton;