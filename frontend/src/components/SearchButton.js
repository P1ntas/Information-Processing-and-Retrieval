import React from 'react';

const SearchButton = ({ onSearch }) => {
  return (
    <button onClick={onSearch}>Search</button>
  );
};

export default SearchButton;
