import React from 'react';
import SearchResultItem from './SearchResultItem';
import SearchBar from './SearchBar';
import SearchButton from './SearchButton';
import FilterOptions from './FilterOptions';
import '../App.css';

const SearchResults = ({ searchQuery }) => {
  // Mock data
  const results = [
    {
      title: 'Lorem Ipsum Dolor Sit Amet',
      content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Sed Do Eiusmod Tempor',
      content: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...'
    },
    {
      title: 'Ut Enim Ad Minim Veniam',
      content: 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris...'
    }
  ];

  return (
    <div className='searchResults'>
      <div className='searchResultsHeader'>
        <div>
          <SearchBar onSearchQueryChange={() => {}} />
          <SearchButton onSearch={() => {}} />
        </div>
        <FilterOptions />
      </div>
      <div className='results'>
        {results.map((result, index) => (
          <SearchResultItem key={index} title={result.title} content={result.content} />
        ))}
      </div>
    </div>
  );
};

export default SearchResults;
