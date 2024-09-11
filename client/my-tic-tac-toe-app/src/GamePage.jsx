import React, { useState } from 'react';
import GameBoard from './GameBoard';

const GamePage = () => {
  const [gameId, setGameId] = useState(null); // Use this for tracking the game session

  return (
    <div>
      <h1>Tic-Tac-Toe</h1>
      <GameBoard gameId={gameId} />
    </div>
  );
};

export default GamePage;
