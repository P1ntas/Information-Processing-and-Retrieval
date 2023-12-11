import React from 'react';

const SearchSuggestionsDropdown = ({ suggestions, onSuggestionClick }) => (
  <div className="searchSuggestionsDropdown">
    {suggestions.map((suggestion, index) => (
      <div key={index} onClick={() => onSuggestionClick(suggestion)}>
        {suggestion}
      </div>
    ))}
  </div>
);

export default SearchSuggestionsDropdown;
