import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const moods = ['Great', 'Good', 'Okay', 'Sad', 'Stressed'];
  const [selectedMood, setSelectedMood] = useState(null);

  const handleStartMeditation = async () => {
    if (!selectedMood) {
      alert('Please select your mood first.');
      return;
    }

    try {
      const response = await axios.post('http://localhost:8000/generate-visualization', {
        emotion: selectedMood,
        focus: 'breathing',
        dream: 'a peaceful place',
        desired_feeling: 'calm and relaxed'
      });
      console.log('Meditation Script:', response.data);
      alert('Meditation script generated! Check the console for details.');
    } catch (error) {
      console.error('Error starting meditation:', error);
      alert('Failed to start meditation. Is the backend running?');
    }
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <span className="navbar-brand">Zen AI</span>
      </nav>
      <main className="main-content">
        <h2>How are you feeling today?</h2>
        <div className="mood-selector">
          {moods.map(mood => (
            <div 
              key={mood} 
              className={`mood-option ${selectedMood === mood ? 'selected' : ''}`}
              onClick={() => setSelectedMood(mood)}
            >
              <div className="mood-icon">😊</div>
              <span>{mood}</span>
            </div>
          ))}
        </div>
        <div className="stats-container">
          <div className="stat-card">
            <div className="stat-icon">⏰</div>
            <div className="stat-title">Today's Meditation</div>
            <div className="stat-value">15 mins</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📅</div>
            <div className="stat-title">Weekly Streak</div>
            <div className="stat-value">5 days</div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">❤️</div>
            <div className="stat-title">Last Session Mood</div>
            <div className="stat-value">Good</div>
          </div>
        </div>
        <button className="meditation-button" onClick={handleStartMeditation}>
          Start Meditation
        </button>
      </main>
    </div>
  );
}

export default App;
