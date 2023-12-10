import React from 'react';
import '../App.css';

const PlayerInfoBox = ({ player }) => {
  if (!player) {
    return null;
  }

  const truncateSummary = (summary, maxLength) => {
    if (summary.length > maxLength) {
      return summary.substring(0, maxLength) + '...';
    }
    return summary;
  };

  const displayedSummary = truncateSummary(player.summary, 400);

  return (
    <div className='playerInfoBox'>
      <img src={player.image_url} alt={player.name} />
      <h2>
        <a href={player.url} target="_blank" rel="noopener noreferrer">
          {player.name}
        </a>
      </h2>
      <p>{displayedSummary}</p>
    </div>
  );
};

export default PlayerInfoBox;
