import React, { useEffect, useState } from 'react';
import SearchResultItem from './SearchResultItem';
import SearchBar from './SearchBar';
import SearchButton from './SearchButton';
import FilterOptions from './FilterOptions';
import '../App.css';
import { useSearchParams } from 'react-router-dom';

const SearchResults = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [searchParams] = useSearchParams();
  const searchQuery = searchParams.get('query');

  useEffect(() => {
    const fetchData = async () => {
      if (searchQuery) {
        try {
          const response = await fetch(`http://localhost:5000/api/search?query=${encodeURIComponent(searchQuery)}`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          setSearchResults(data.articles.results);
        } catch (error) {
          console.error("Error fetching data", error);
        }
      }
    };

    fetchData();
  }, [searchQuery]);

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
        {searchResults.map((article) => (
          <SearchResultItem 
            key={article.id}
            title={article.title} 
            summary={article.summary} 
            url={article.url} 
          />
        ))}
      </div>
    </div>
  );
};

export default SearchResults;
