import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import QuizPage from './pages/QuizPage';
import MeditationPage from './pages/MeditationPage';
import VisualizationCoachScreen from './pages/VisualizationCoachScreen';
import MeditationQuestionnaireScreen from './pages/MeditationQuestionnaireScreen';
import { AppProvider } from './context/AppContext';
import { VisualizationProvider } from './context/VisualizationContext';

function App() {
  return (
    <AppProvider>
      <VisualizationProvider>
        <Router>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/quiz" element={<QuizPage />} />
            <Route path="/coach" element={<VisualizationCoachScreen />} />
            <Route path="/meditation-questionnaire" element={<MeditationQuestionnaireScreen />} />
            <Route path="/meditate" element={<MeditationPage />} />
          </Routes>
        </Router>
      </VisualizationProvider>
    </AppProvider>
  );
}

export default App;
