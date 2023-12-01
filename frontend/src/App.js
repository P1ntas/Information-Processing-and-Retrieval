import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import SearchBar from './components/SearchBar';
import SearchButton from './components/SearchButton';
import SearchResults from './components/SearchResults';
import './App.css';

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
    <div>
      <h1>My Search Engine</h1>
      <SearchBar onSearchQueryChange={handleSearchQueryChange} />
      <SearchButton onSearch={handleSearch} />
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
