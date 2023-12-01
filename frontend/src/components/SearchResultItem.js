import React from 'react';
import '../App.css';


const SearchResultItem = ({ title, content }) => {
  return (
    <div className="search-result-item">
      <h3><a href="#">{title}</a></h3>
      <p>{content}</p>
    </div>
  );
};

export default SearchResultItem;
