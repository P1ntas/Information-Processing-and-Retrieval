import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../App.css';

const TeamPage = () => {
  const [team, setTeam] = useState(null);
  const { teamAbbreviation } = useParams();

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

  if (!team) {
    return <div>Loading...</div>;
  }

  return (
    <div className="page-container team-page">
      <img src={team.image_url} alt={team.name} className="page-image" />
      <h1 className="page-title">{team.name}</h1>
      <p className="page-summary">{team.summary}</p>
    </div>
  );
};

export default TeamPage;
