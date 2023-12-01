import React from 'react';

const SearchBar = ({ onSearchQueryChange }) => {
  return (
    <input
      type="text"
      placeholder="Search..."
      onChange={(e) => onSearchQueryChange(e.target.value)}
    />
  );
};

export default SearchBar;
