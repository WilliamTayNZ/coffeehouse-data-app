import { createContext, useContext, useState } from "react";

const SheetsContext = createContext();

export const useSheetsContext = () => useContext(SheetsContext);

export const SheetsProvider = ({ children }) => {
  const [cleanedSheets, setCleanedSheets] = useState({});
  const [selectedSheet, setSelectedSheet] = useState(null);

  // Set all cleaned sheets after cleaning
  const setAllCleanedSheets = (sheetsDict) => {
    setCleanedSheets(sheetsDict);
    setSelectedSheet(Object.keys(sheetsDict)[0] || null); // Default to first sheet
  };

  // Update summary, insights, or results for a sheet
  const updateSheetData = (sheetName, newData) => {
    setCleanedSheets(prev => ({
      ...prev,
      [sheetName]: {
        ...prev[sheetName],
        ...newData,
      }
    }));
  };

  return (
    <SheetsContext.Provider value={{
      cleanedSheets,
      selectedSheet,
      setAllCleanedSheets,
      setSelectedSheet,
      updateSheetData,
    }}>
      {children}
    </SheetsContext.Provider>
  );
};