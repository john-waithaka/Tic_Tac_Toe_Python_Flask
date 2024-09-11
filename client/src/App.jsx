

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/auth/Login';
import RegisterForm from './components/auth/RegisterForm';  // Updated import
import GridSizeSelection from './components/game/GridSizeSelection';
import GameBoard from './components/game/GameBoard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterForm />} />  {/* Use RegisterForm component */}
        <Route path="/choose-grid" element={<GridSizeSelection />} />
        <Route path="/game/:gridSize" element={<GameBoard />} />
      </Routes>
    </Router>
  );
}

export default App;


