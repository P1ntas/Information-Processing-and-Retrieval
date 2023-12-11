import React, { useEffect, useState } from 'react';
import SearchResultItem from './SearchResultItem';
import SearchBar from './SearchBar';
import SearchButton from './SearchButton';
import '../App.css';
import { useSearchParams, useNavigate } from 'react-router-dom';
import PlayerInfoBox from './PlayerInfoBox';

const SearchResults = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [searchSpelling, setSearchSpelling] = useState(null); // TODO: Implement this
  const [playerInfo, setPlayerInfo] = useState(null);
  const [teamInfo, setTeamInfo] = useState(null);
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const initialQuery = searchParams.get('query')?.trim() || '';
  const [searchQuery, setSearchQuery] = useState(initialQuery);

  const handleArticleClick = (articleId) => {
    navigate(`/article/${articleId}`);
  };

  const handleSearchQueryChange = (query) => {
    setSearchQuery(query);
  };

  const handleSearch = () => {
    navigate(`/search?query=${encodeURIComponent(searchQuery)}`);
  };

  const handleSpellingClick = (spelling) => {
    setSearchQuery(spelling);
    navigate(`/search?query=${encodeURIComponent(spelling)}`);
  }


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
          setSearchSpelling(data.articles.collation);
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
      </div>
      <div className='resultsLayout'>
        <div className='results'>
          {searchSpelling && (
            <div className='searchSpelling'>
              <p>
              Did you mean: <b onClick={() => handleSpellingClick(searchSpelling)} className="searchSpellingLink" style={{ cursor: 'pointer' }}>{searchSpelling}</b>
              </p>
            </div>
          )}
          {searchResults.map((article) => (
            <SearchResultItem 
              key={article.id}
              id={article.id}
              title={article.title} 
              summary={article.summary}
              onClick={() => handleArticleClick(article.id)}          
            />
          ))}
        </div>
        <PlayerInfoBox player={playerInfo} team={teamInfo} />
      </div>
    </div>
  );
};

export default SearchResults;
