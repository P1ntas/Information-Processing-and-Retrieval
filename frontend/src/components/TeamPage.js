import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import SearchBar from './SearchBar';
import SearchButton from './SearchButton';
import '../App.css';

const TeamPage = () => {
  const [team, setTeam] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const { teamAbbreviation } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTeam = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/team/${encodeURIComponent(teamAbbreviation)}`);
        if (!response.ok) {
          throw new Error('Team fetch failed');
        }
        const data = await response.json();
        setTeam(data);
      } catch (error) {
        console.error('Error fetching team:', error);
      }
    };

    if (teamAbbreviation) {
        fetchTeam();
    }
  }, [teamAbbreviation]);

  const handleSearchQueryChange = (query) => {
    setSearchQuery(query);
  };

  const handleSearch = () => {
    if (teamAbbreviation && searchQuery) {
      navigate(`/search?team=${encodeURIComponent(teamAbbreviation)}&query=${encodeURIComponent(searchQuery)}`);
    }
  };

  if (!team) {
    return <div>Loading...</div>;
  }

  return (
    <div className="page-container team-page">
      <div className="search-container">
        <SearchBar onSearchQueryChange={handleSearchQueryChange} />
        <SearchButton onSearch={handleSearch} />
      </div>
      <img src={team.image_url} alt={team.name} className="page-image" />
      <h1 className="page-title">{team.name}</h1>
      <p className="page-summary">{team.summary}</p>
    </div>
  );
};

export default TeamPage;
