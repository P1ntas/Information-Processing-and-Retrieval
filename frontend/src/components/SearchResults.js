import React from 'react';
import SearchResultItem from './SearchResultItem';
import SearchBar from './SearchBar';
import SearchButton from './SearchButton';
import FilterOptions from './FilterOptions';
import '../App.css';

const SearchResults = ({ searchQuery }) => {
  // Mock data
  const results = {
    "team": {}, 
    "player": {},
    "articles": [
      {
        "id": "3908", 
        "title": "GW26 Differentials: Sadio Mane", 
        "summary": "The Scout on why wi matches ", 
        "text": "\n The Scout is tipping four low-owned pl\n", 
        "date": "2022-02-17T00:00:00Z", 
        "url": "https://www.premierleague.com/news/2488660", 
        "_version_": 1784807969405272064, 
        "score": 160.5178
      },
      {
        "id": "3908", 
        "title": "GW26 Differentials: Sadio Mane", 
        "summary": "The Scout on why wi matches ", 
        "text": "\n The Scout is tipping four low-owned pl\n", 
        "date": "2022-02-17T00:00:00Z", 
        "url": "https://www.premierleague.com/news/2488660", 
        "_version_": 1784807969405272064, 
        "score": 160.5178
      },
      {
        "id": "3908", 
        "title": "GW26 Differentials: Sadio Mane", 
        "summary": "The Scout on why wi matches ", 
        "text": "\n The Scout is tipping four low-owned pl\n", 
        "date": "2022-02-17T00:00:00Z", 
        "url": "https://www.premierleague.com/news/2488660", 
        "_version_": 1784807969405272064, 
        "score": 160.5178
      },
    ]
  };

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
        {results.articles.map((article, index) => (
          <SearchResultItem 
            key={article.id} // It's better to use unique identifiers like 'id' for the key
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
