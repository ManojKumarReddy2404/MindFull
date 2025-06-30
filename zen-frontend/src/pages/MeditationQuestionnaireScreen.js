import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
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

const MeditationQuestionnaireScreen = () => {
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState({});
    const [freeText, setFreeText] = useState('');
    const navigate = useNavigate();
    const { setVisualizationData } = useContext(VisualizationContext);

    // State for handling the API response
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

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
            setVisualizationData(newAnswers); // Save final answers to context
            setIsLoading(true);
            setError(null);

            try {
                const meditationInput = {
                    quiz_answers: Object.values(newAnswers),
                    user_input: "Generate a meditation based on my answers.",
                    voice_pref: "alloy", // Default voice
                    music_pref: "Calm" // Default music style
                };

                console.log("Sending to /meditate:", meditationInput);

                const response = await fetch('http://localhost:8000/meditate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(meditationInput),
                    timeout: 120000, // 2 minutes timeout for AI generation
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                console.log('Backend Response:', data);
                if (data.meditation_text) {
                    navigate('/meditate', { state: { meditation: data } });
                } else {
                    throw new Error('Failed to get meditation data from backend.');
                }

            } catch (e) {
                console.error('Error fetching meditation:', e);
                setError('Failed to generate your meditation. Please try again.');
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
        setError(null);
    };

    // Render loading state
    if (isLoading) {
        return (
            <div className="coach-screen">
                <div className="coach-container">
                    <p className="coach-question">Generating your personalized meditation...</p>
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

export default MeditationQuestionnaireScreen;
