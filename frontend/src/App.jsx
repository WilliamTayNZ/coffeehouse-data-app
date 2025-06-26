import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home.jsx';
import CleaningSummary from './pages/CleaningSummary.jsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/:filename/cleaning-summary" element={<CleaningSummary />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
