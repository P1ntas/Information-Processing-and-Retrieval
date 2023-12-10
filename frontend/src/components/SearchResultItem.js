import React from 'react';
import '../App.css';


const SearchResultItem = ({ title, summary, url }) => {
  return (
    <div className="search-result-item">
      <h3><a href={url} target="_blank" rel="noopener noreferrer">{title}</a></h3>
      <p>{summary}</p>
    </div>
  );
};

export default SearchResultItem;
