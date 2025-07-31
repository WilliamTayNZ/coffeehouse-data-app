import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home.jsx';
import CleanNewFile from './pages/CleanNewFile.jsx';
import CleaningSummary from './pages/CleaningSummary.jsx';
import CleanedSheets from './pages/CleanedSheets.jsx';

import { SheetsProvider } from './contexts/SheetsContext.jsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cleaned-sheets" element={<CleanedSheets />} />
        <Route path="/clean-new-file" element={<CleanNewFile />} />
        <Route path="/:filename/cleaning-summary" element={<CleaningSummary />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
