import React from 'react';
import '../App.css';

const SearchResultItem = ({ id, title, summary, onClick }) => {
  return (
    <div className="search-result-item" onClick={() => onClick(id)}>
      <h3>{title}</h3>
      <p>{summary}</p>
    </div>
  );
};

export default SearchResultItem;
