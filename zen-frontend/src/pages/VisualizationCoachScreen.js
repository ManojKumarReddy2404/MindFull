import React, { useState, useContext } from 'react';

import { VisualizationContext } from '../context/VisualizationContext';
import './VisualizationCoachScreen.css';

const questions = [
    {
        key: 'emotion',
        text: 'How are you feeling right now?',
        options: ['Happy', 'Sad', 'Anxious', 'Calm', 'Excited', 'Tired'],
    },
    {
        key: 'focus',
        text: 'What’s been on your mind lately?',
        options: ['Work', 'Relationships', 'Health', 'Future', 'Creativity', 'Nothing much'],
    },
    {
        key: 'dream',
        text: 'What’s one thing you wish was true in your life?',
        options: ['Financial freedom', 'Better relationships', 'Career success', 'Inner peace', 'Good health', 'More travel'],
    },
    {
        key: 'desired_feeling',
        text: 'What do you want to feel more of?',
        options: ['Peace', 'Joy', 'Confidence', 'Motivation', 'Clarity', 'Gratitude'],
    },
];

const VisualizationCoachScreen = () => {
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState({});
    const [freeText, setFreeText] = useState('');
    const { setVisualizationData } = useContext(VisualizationContext);

    // State for handling the API response
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [visualizationSession, setVisualizationSession] = useState(null); // Changed from plan to visualizationSession

    const handleOptionClick = (option) => {
        handleNext(option);
    };

    const handleFreeTextChange = (e) => {
        setFreeText(e.target.value);
    };

    const handleNext = async (value) => {
        const currentQuestion = questions[currentQuestionIndex];
        const newAnswers = { ...answers, [currentQuestion.key]: value };
        setAnswers(newAnswers);
        setFreeText('');

        if (currentQuestionIndex < questions.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
        } else {
            // Last question answered, now call the backend
            setVisualizationData(newAnswers); // Save final answers to context
            setIsLoading(true);
            setError(null);

            try {
                console.log("Sending to /visualize:", newAnswers);

                const response = await fetch('http://localhost:8000/visualize', { // Updated endpoint
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(newAnswers), // Updated body
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                    throw new Error(`HTTP error! status: ${response.status}, details: ${errorData.detail}`);
                }

                const data = await response.json();
                console.log('Backend Response:', data);
                setVisualizationSession(data); // Updated state setter

            } catch (e) {
                console.error('Error fetching visualization session:', e);
                setError(e.message || 'Failed to generate your session. Please try again.');
            } finally {
                setIsLoading(false);
            }
        }
    };

    const handleSkip = () => {
        handleNext('Not sure');
    };

    const handleRestart = () => {
        setCurrentQuestionIndex(0);
        setAnswers({});
        setVisualizationSession(null); // Updated state reset
        setError(null);
    };

    // Render loading state
    if (isLoading) {
        return (
            <div className="coach-screen">
                <div className="coach-container">
                    <p className="coach-question">Generating your personalized visualization...</p>
                    <div className="loader"></div>
                </div>
            </div>
        );
    }

    // Render error state
    if (error) {
        return (
            <div className="coach-screen">
                <div className="coach-container">
                    <p className="coach-question">{error}</p>
                    <button className="option-chip" onClick={handleRestart}>Try Again</button>
                </div>
            </div>
        );
    }

    // Render the generated visualization session
    if (visualizationSession) {
        return (
            <div className="coach-screen">
                <div className="coach-container">
                    <h2 className="plan-title">Your Visualization Journey</h2>
                    <p className="visualization-text">{visualizationSession.visualization_text}</p>
                    <div className="audio-player-container">
                        <h3>Voice</h3>
                        <audio controls src={visualizationSession.voice_output} className="audio-player">
                            Your browser does not support the audio element.
                        </audio>
                        <h3>Music</h3>
                        <audio controls src={visualizationSession.music_output} className="audio-player">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                    <button className="option-chip" onClick={handleRestart}>Start Over</button>
                </div>
            </div>
        );
    }

    // Render the current question
    const currentQuestion = questions[currentQuestionIndex];
    return (
        <div className="coach-screen">
            <div className="coach-container">
                <p className="coach-question">{currentQuestion.text}</p>
                <div className="options-container">
                    {currentQuestion.options.map((option) => (
                        <button key={option} className="option-chip" onClick={() => handleOptionClick(option)}>
                            {option}
                        </button>
                    ))}
                </div>
                <div className="free-text-container">
                    <input
                        type="text"
                        className="free-text-input"
                        placeholder="Or type your own..."
                        value={freeText}
                        onChange={handleFreeTextChange}
                        onKeyDown={(e) => e.key === 'Enter' && freeText.trim() && handleNext(freeText.trim())}
                    />
                    <button className="send-button" onClick={() => freeText.trim() && handleNext(freeText.trim())} disabled={!freeText.trim()}>
                        &#10148;
                    </button>
                </div>
                <button className="skip-button" onClick={handleSkip}>
                    Skip
                </button>
            </div>
        </div>
    );
};

export default VisualizationCoachScreen;
