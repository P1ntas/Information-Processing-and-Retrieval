import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import SearchBar from './components/SearchBar';
import SearchButton from './components/SearchButton';
import SearchResults from './components/SearchResults';
import FilterOptions from './components/FilterOptions';
import './App.css';
import logo from './images/logo.png';

function SearchPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearchQueryChange = (query) => {
    setSearchQuery(query);
  };

  const handleSearch = () => {
    navigate(`/search?query=${searchQuery}`);
  };

  return (
    <div className="search-page-container">
      <div className="title">
        <img src={logo} alt="Premier League Logo" />
        <h1>Premier League</h1>
      </div>
      <div className="search-container">
        <div className="search-inputs">
          <SearchBar onSearchQueryChange={handleSearchQueryChange} />
          <SearchButton onSearch={handleSearch} />
        </div>
        <FilterOptions />
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
          </Routes>
        </header>
      </div>
    </Router>
  );
}

export default App;
