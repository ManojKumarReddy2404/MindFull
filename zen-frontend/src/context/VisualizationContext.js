import React, { createContext, useState } from 'react';

export const VisualizationContext = createContext();

export const VisualizationProvider = ({ children }) => {
    const [visualizationData, setVisualizationData] = useState(null);

    return (
        <VisualizationContext.Provider value={{ visualizationData, setVisualizationData }}>
            {children}
        </VisualizationContext.Provider>
    );
};
