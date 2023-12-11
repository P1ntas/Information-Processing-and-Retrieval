import React, { useEffect, useState } from 'react';
import SearchResultItem from './SearchResultItem';
import SearchBar from './SearchBar';
import SearchButton from './SearchButton';
import '../App.css';
import { useSearchParams, useNavigate } from 'react-router-dom';
import PlayerInfoBox from './PlayerInfoBox';

const SearchResults = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [playerInfo, setPlayerInfo] = useState(null);
  const [teamInfo, setTeamInfo] = useState(null);
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchSpelling, setSearchSpelling] = useState(null);
  const navigate = useNavigate();
  const currentQuery = searchParams.get('query')?.trim();
  const currentPlayer = searchParams.get('player')?.trim();
  const initialQuery = searchParams.get('query')?.trim() || '';
  const [searchQuery, setSearchQuery] = useState(initialQuery);

  const handleArticleClick = (articleId) => {
    navigate(`/article/${articleId}`);
  };

  const handleSpellingClick = (spelling) => {
    setSearchQuery(spelling);
    navigate(`/search?query=${encodeURIComponent(spelling)}`);
  }

  const handleSearchQueryChange = (query) => {
    setSearchQuery(query);
  };

  const handleSearch = () => {
    navigate(`/search?query=${encodeURIComponent(searchQuery)}`);
  };

  useEffect(() => {
    const fetchData = async () => {
      const currentQuery = searchParams.get('query')?.trim();
      const currentPlayer = searchParams.get('player')?.trim();
      const currentTeam = searchParams.get('team')?.trim();

      let url;
      if (currentPlayer && currentQuery) {
        url = `http://127.0.0.1:5000/api/player/${encodeURIComponent(currentPlayer)}/search?query=${encodeURIComponent(currentQuery)}`;
      } else if (currentTeam && currentQuery) {
        url = `http://127.0.0.1:5000/api/team/${encodeURIComponent(currentTeam)}/search?query=${encodeURIComponent(currentQuery)}`;
      } else if (currentQuery) {
        url = `http://127.0.0.1:5000/api/search?query=${encodeURIComponent(currentQuery)}`;
      }

      if (url) {
        try {
          const response = await fetch(url);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          // Handle different response structures
          if (data.articles) {
            setSearchResults(data.articles.results);
            setSearchSpelling(data.articles.collation);
            setPlayerInfo(null);
            setTeamInfo(null);
          } else {
            setSearchResults(data.results);
            if (currentPlayer) {
              setPlayerInfo({ name: currentPlayer });
            }
            else if (currentTeam) {
              setTeamInfo({ name: currentTeam }); // Adjust based on your data structure
            }
          }
        // Check and set playerInfo and teamInfo based on response
        if (data.player) {
          setPlayerInfo(data.player);
        } else {
          setPlayerInfo(null); // Clear if no player data
        }

        if (data.team) {
          setTeamInfo(data.team);
        } else {
          setTeamInfo(null); // Clear if no team data
        }
      } catch (error) {
        console.error("Error fetching data", error);
      }
      }
    };

    fetchData();
  }, [searchParams]);
  

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
               Did you mean: <b onClick={() => handleSpellingClick(searchSpelling)} className="searchSpellingLink">{searchSpelling}</b>
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
