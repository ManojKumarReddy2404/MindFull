import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css';

function HomePage() {
  return (
    <div className="container">
      <header className="header">
        <h1>Welcome to Zen Focus</h1>
        <p>Your personal guide to mindfulness and meditation.</p>
      </header>
      <main className="main-content">
        <p>Choose your path to a calmer mind:</p>
        <div className="button-container">
          <Link to="/meditation-questionnaire" className="btn-primary">Start Meditation</Link>
          <Link to="/coach" className="btn-secondary">Start Visualization</Link>
        </div>
      </main>
    </div>
  );
}

export default HomePage;
