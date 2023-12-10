import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const PlayerInfoBox = ({ player, team }) => {
  const navigate = useNavigate();
  let info = player || team;

  if (!info) {
    return null;
  }

  const handleInfoClick = () => {
    if (player) {
      navigate(`/player/${encodeURIComponent(player.name)}`);
    } else if (team) {
        navigate(`/team/${encodeURIComponent(team.abbreviation)}`);
    }
  };

  const truncateSummary = (summary, maxLength) => {
    if (summary.length > maxLength) {
      return summary.substring(0, maxLength) + '...';
    }
    return summary;
  };

  const displayedSummary = truncateSummary(info.summary, 400);

  return (
    <div className='playerInfoBox'>
      <img src={info.image_url} alt={info.name} />
      <h2 onClick={handleInfoClick}>
        {info.name}
      </h2>
      <p>{displayedSummary}</p>
    </div>
  );
};

export default PlayerInfoBox;
