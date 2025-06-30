import React from 'react';
import { useLocation } from 'react-router-dom';
import './MeditationPage.css';

function MeditationPage() {
  const location = useLocation();
  const { meditation } = location.state || {};

  if (!meditation) {
    return (
      <div className="meditation-container">
        <h1>Meditation Session</h1>
        <p>No meditation data found. Please start from the home page.</p>
      </div>
    );
  }

  return (
    <div className="meditation-container">
      <h1 className="meditation-title">Your Personalized Session</h1>
      <div className="meditation-content">
        <p className="meditation-script">{meditation.meditation_text}</p>
      </div>
      <div className="audio-controls">
        <div className="audio-player">
          <h2>Guided Voice</h2>
          <audio controls src={meditation.voice_output}>
            Your browser does not support the audio element.
          </audio>
        </div>
        <div className="audio-player">
          <h2>Background Music</h2>
          <audio controls loop src={meditation.music_output}>
            Your browser does not support the audio element.
          </audio>
        </div>
      </div>
    </div>
  );
}

export default MeditationPage;
