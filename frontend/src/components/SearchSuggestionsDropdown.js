import React, { useState, useRef, useEffect } from 'react';

const SearchSuggestionsDropdown = ({ searchSuggestions, handleSuggestionClick }) => {
  const [isDropdownVisible, setDropdownVisibility] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    document.addEventListener('click', handleDocumentClick);

    return () => {
      document.removeEventListener('click', handleDocumentClick);
    };
  }, []);

  useEffect(() => {
    // This useEffect will run whenever searchSuggestions changes
    // You can perform any necessary actions here when the prop changes
    // For example, you can show/hide the dropdown based on the prop change
    setDropdownVisibility(searchSuggestions.length > 0);
  }, [searchSuggestions]);

  const handleDocumentClick = (event) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
      setDropdownVisibility(false);
    }
  };

  return (
    <div className='searchSuggestions'>
      {searchSuggestions.length > 0 && isDropdownVisible && (
        <div ref={dropdownRef} className='searchSuggestionsDropdown'>
          {searchSuggestions.map((suggestion, index) => (
            <div
              key={index}
              onClick={() => {
                handleSuggestionClick(suggestion);
                setDropdownVisibility(false);
              }}
            >
              {suggestion}
            </div>
          ))}
        </div>
      )}
      {/* Other components or buttons */}
    </div>
  );
};

export default SearchSuggestionsDropdown;
