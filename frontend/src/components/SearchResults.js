import React, { useEffect, useState } from 'react';
import SearchResultItem from './SearchResultItem';
import SearchBar from './SearchBar';
import SearchButton from './SearchButton';
import '../App.css';
import { useSearchParams, useNavigate } from 'react-router-dom';
import PlayerInfoBox from './PlayerInfoBox';
import SearchSuggestionsDropdown from './SearchSuggestionsDropdown';

const SearchResults = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [playerInfo, setPlayerInfo] = useState(null);
  const [teamInfo, setTeamInfo] = useState(null);
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchSpelling, setSearchSpelling] = useState(null);
  const navigate = useNavigate();
  const currentQuery = searchParams.get('query')?.trim();
  const currentPlayer = searchParams.get('player')?.trim();
  const currentTeam = searchParams.get('team')?.trim();
  const initialQuery = searchParams.get('query')?.trim() || '';
  const [searchQuery, setSearchQuery] = useState(initialQuery);
  const [searchSuggestions, setSearchSuggestions] = useState([]);

  const handleArticleClick = (articleId) => {
    navigate(`/article/${articleId}`);
  };

  const handleSpellingClick = (spelling) => {
    setSearchQuery(spelling);
    navigate(`/search?query=${encodeURIComponent(spelling)}`);
  };


  const handleSuggestionClick = (suggestion) => {
    setSearchQuery(suggestion);
    navigate(`/search?query=${encodeURIComponent(suggestion)}`);
  };

  const handleSearchQueryChange = (query) => {
    setSearchQuery(query);
    fetchSearchSuggestions(query);
  };

  const fetchSearchSuggestions = async (query) => {
    const url = `http://127.0.0.1:5000/api/suggest?query=${encodeURIComponent(query)}`;
    try {
      const response = await fetch(url);
      if (response.ok) {
        const suggestions = await response.json();
        console.log(suggestions)
        setSearchSuggestions(suggestions)
      } else {
        console.error('Error fetching search suggestions:', response.status);
        return [];
      }
    } catch (error) {
      console.error('Error fetching search suggestions:', error);
      return [];
    }
  };

  const isSpecificSearch = currentPlayer || currentTeam;

  const handleSearch = () => {
    if (currentPlayer) {
      navigate(`/search?player=${encodeURIComponent(currentPlayer)}&query=${encodeURIComponent(searchQuery)}`);
    } else if (currentTeam) {
      navigate(`/search?team=${encodeURIComponent(currentTeam)}&query=${encodeURIComponent(searchQuery)}`);
    } else {
      navigate(`/search?query=${encodeURIComponent(searchQuery)}`);
    }
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

          // Set search results
          setSearchResults(data.results || (data.articles && data.articles.results) || []);

          if (data.articles) {
            setSearchSpelling(data.articles.collation);
          }
          
          if (data.player) {
            setPlayerInfo(data.player);
          } else if (!currentPlayer) {
            setPlayerInfo(null);
          }

          if (data.team) {
            setTeamInfo(data.team);
          } else if (!currentTeam) {
            setTeamInfo(null);
          }

          // Fetch and set player or team info if specific search
          if (currentPlayer) {
            const playerResponse = await fetch(`http://127.0.0.1:5000/api/player/${encodeURIComponent(currentPlayer)}`);
            const playerData = await playerResponse.json();
            setPlayerInfo(playerData);
          }

          if (currentTeam) {
            const teamResponse = await fetch(`http://127.0.0.1:5000/api/team/${encodeURIComponent(currentTeam)}`);
            const teamData = await teamResponse.json();
            setTeamInfo(teamData);
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
      <div className='searchResultsContainer'>
        <div className='searchResultsHeader'>
          <SearchBar onSearchQueryChange={handleSearchQueryChange} />
          <SearchButton onSearch={handleSearch} />
        </div>
        <SearchSuggestionsDropdown
            searchSuggestions={searchSuggestions}
            handleSuggestionClick={handleSuggestionClick}
          />
      </div>

      <div className='resultsLayout'>
        <div className='results'>
          {searchSpelling && (
            <div className='searchSpelling'>
              <p>
                Did you mean: <b onClick={() => handleSpellingClick(searchSpelling)} className='searchSpellingLink'>{searchSpelling}</b>
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
        {isSpecificSearch && (
          <button onClick={() => navigate('/')} className="backToHomeButton">Back to Home</button>
        )}
    </div>
  );
};

export default SearchResults;
