import React, { useEffect, useState } from 'react';
import SearchResultItem from './SearchResultItem';
import SearchBar from './SearchBar';
import SearchButton from './SearchButton';
import FilterOptions from './FilterOptions';
import '../App.css';
import { useSearchParams, useNavigate } from 'react-router-dom';
import PlayerInfoBox from './PlayerInfoBox';

const SearchResults = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [playerInfo, setPlayerInfo] = useState(null);
  const [teamInfo, setTeamInfo] = useState(null);
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const initialQuery = searchParams.get('query')?.trim() || '';
  const [searchQuery, setSearchQuery] = useState(initialQuery);

  const handleSearchQueryChange = (query) => {
    setSearchQuery(query);
  };

  const handleSearch = () => {
    navigate(`/search?query=${encodeURIComponent(searchQuery)}`);
  };

  useEffect(() => {
    const fetchData = async () => {
      if (searchQuery) {
        try {
          const url = `http://127.0.0.1:5000/api/search?query=${encodeURIComponent(searchQuery)}`;
          const response = await fetch(url, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            }
          });
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          setSearchResults(data.articles.results);
          setPlayerInfo(data.player);  // Assuming 'player' is part of the returned data
          if (data.player) {
            setPlayerInfo(data.player);
            setTeamInfo(null); // Clear team info if player info is available
          } else if (data.team) {
            setTeamInfo(data.team);
            setPlayerInfo(null); // Clear player info if team info is available
          } else {
            setPlayerInfo(null);
            setTeamInfo(null);
          }
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
          <SearchBar onSearchQueryChange={handleSearchQueryChange} />
          <SearchButton onSearch={handleSearch} />
        </div>
        <FilterOptions />
      </div>
      <div className='resultsLayout'>
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
        <PlayerInfoBox player={playerInfo} team={teamInfo} />
      </div>
    </div>
  );
};

export default SearchResults;
