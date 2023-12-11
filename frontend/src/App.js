import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import SearchBar from './components/SearchBar';
import SearchButton from './components/SearchButton';
import SearchResults from './components/SearchResults';
import ArticlePage from './components/ArticlePage';
import PlayerPage from './components/PlayerPage';
import TeamPage from './components/TeamPage';
import SearchSuggestionsDropdown from './components/SearchSuggestionsDropdown';
import './App.css';
import logo from './images/logo.png';

function SearchPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchSuggestions, setSearchSuggestions] = useState([]);
  const navigate = useNavigate();

  const handleSearchQueryChange = (query) => {
    setSearchQuery(query);
    fetchSearchSuggestions(query);
  };

  const handleSearch = () => {
    navigate(`/search?query=${searchQuery}`);
  };

  const handleSuggestionClick = (suggestion) => {
    setSearchQuery(suggestion);
    navigate(`/search?query=${encodeURIComponent(suggestion)}`);
  };

  const fetchSearchSuggestions = async (query) => {
    const url = `http://127.0.0.1:5000/api/suggest?query=${encodeURIComponent(query)}`;
    try {
      const response = await fetch(url);
      if (response.ok) {
        const suggestions = await response.json();
        console.log(suggestions);
        setSearchSuggestions(suggestions);
      } else {
        console.error('Error fetching search suggestions:', response.status);
        return [];
      }
    } catch (error) {
      console.error('Error fetching search suggestions:', error);
      return [];
    }
  };

  return (
    <div className="search-page-container">
      <div className="title">
        <img src={logo} alt="Premier League Logo" />
        <h1>Premier League</h1>
      </div>
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
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/search" element={<SearchResults />} />
            <Route path="/article/:articleId" element={<ArticlePage />} />
            <Route path="/player/:playerName" element={<PlayerPage />} />
            <Route path="/team/:teamAbbreviation" element={<TeamPage />} />
          </Routes>
        </header>
      </div>
    </Router>
  );
}

export default App;
