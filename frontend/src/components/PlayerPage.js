import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../App.css';

const PlayerPage = () => {
  const [player, setPlayer] = useState(null);
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

  if (!player) {
    return <div>Loading...</div>;
  }

  return (
    <div className="page-container player-page">
      <img src={player.image_url} alt={player.name} className="page-image" />
      <h1 className="page-title">{player.name}</h1>
      <p className="page-summary">{player.summary}</p>
    </div>
  );
};

export default PlayerPage;
