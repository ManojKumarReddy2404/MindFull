import React, { createContext, useState, useContext } from 'react';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [quizAnswers, setQuizAnswers] = useState([]);
  const [userInput, setUserInput] = useState('');

  const value = {
    quizAnswers,
    setQuizAnswers,
    userInput,
    setUserInput,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useAppContext = () => {
  return useContext(AppContext);
};
