import React from 'react';
import filter from '../images/filter.png';
import '../App.css';

const FilterOptions = () => {
  return (
    <div className="filter-container">
      <div className="filter-label">
      <img src={filter} alt="Filter" />
        Filters</div>
      <div className="filter-options">
        <div className="filter-option">Games</div>
        <div className="filter-option">News</div>
        <div className="filter-option">Players</div>
      </div>
    </div>
  );
};

export default FilterOptions;