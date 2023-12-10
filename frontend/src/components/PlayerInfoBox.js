import React from 'react';
import '../App.css';

const PlayerInfoBox = ({ player, team }) => {
  let info = player || team;

  if (!info) {
    return null;
  }

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
      <h2>
        <a href={info.url} target="_blank" rel="noopener noreferrer">
          {info.name}
        </a>
      </h2>
      <p>{displayedSummary}</p>
    </div>
  );
};

export default PlayerInfoBox;
