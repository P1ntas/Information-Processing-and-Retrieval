import React from 'react';
import '../App.css';

const SearchButton = ({ onSearch }) => {
  return (
    <button onClick={onSearch}>Search</button>
  );
};

export default SearchButton;
