import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import SearchBar from './SearchBar';
import SearchButton from './SearchButton';
import '../App.css';

const PlayerPage = () => {
  const [player, setPlayer] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const { playerName } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPlayer = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/player/${encodeURIComponent(playerName)}`);
        if (!response.ok) {
          throw new Error('Player fetch failed');
        }
        const data = await response.json();
        setPlayer(data);
      } catch (error) {
        console.error('Error fetching player:', error);
      }
    };

    if (playerName) {
      fetchPlayer();
    }
  }, [playerName]);

  const handleTeamClick = (abbreviation) => {
    navigate(`/team/${encodeURIComponent(abbreviation)}`);
  };

  const handleSearchQueryChange = (query) => {
    setSearchQuery(query);
  };

  const handleSearch = async () => {
    if (playerName && searchQuery) {   
      navigate(`/search?player=${encodeURIComponent(playerName)}&query=${encodeURIComponent(searchQuery)}`);
    }
  };

  if (!player) {
    return <div>Loading...</div>;
  }

  const { player_stats } = player;

  return (
    <div className="page-container player-page">
      <div className="search-container">
        <SearchBar onSearchQueryChange={handleSearchQueryChange} />
        <SearchButton onSearch={handleSearch} />
      </div>
      <img src={player.image_url} alt={player.name} className="page-image" />
      <h1 className="page-title">{player.name}</h1>
      <p className="page-summary">{player.summary}</p>
      <h2>Player Statistics</h2>
      <table className="player-stats-table">
        <tbody>
          <tr><td>Number of Games:</td><td>{player_stats.nr_games}</td></tr>
          <tr><td>Goals:</td><td>{player_stats.goals}</td></tr>
          <tr><td>Assists:</td><td>{player_stats.assists}</td></tr>
          <tr><td>Yellow Cards:</td><td>{player_stats.yellow_cards}</td></tr>
          <tr><td>Double Yellow Cards:</td><td>{player_stats.double_yellow_cards}</td></tr>
          <tr><td>Red Cards:</td><td>{player_stats.red_cards}</td></tr>
          <tr><td>Minutes Played:</td><td>{player_stats.minutes_played}</td></tr>
          <tr><td>Season:</td><td>{player_stats.season}</td></tr>
          <tr>
            <td>Team:</td>
            <td>
              <span
                className="team-link"
                onClick={() => handleTeamClick(player_stats.abbreviation)}
              >
                {player_stats.team}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default PlayerPage;
