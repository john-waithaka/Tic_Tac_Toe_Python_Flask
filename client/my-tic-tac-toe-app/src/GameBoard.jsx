import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GameBoard = ({ gameId }) => {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [xIsNext, setXIsNext] = useState(true);

  useEffect(() => {
    // Fetch the current game state from the backend
    const fetchGameState = async () => {
      try {
        const response = await axios.get(`/api/game/${gameId}`);
        setBoard(response.data.board);
        setXIsNext(response.data.xIsNext);
      } catch (error) {
        console.error('Error fetching game state:', error);
      }
    };
    
    if (gameId) fetchGameState();
  }, [gameId]);

  const handleClick = (index) => {
    // Handle the click event and update the board
    // Make a POST request to update the game state on the backend
  };

  return (
    <div>
      <div>
        {board.map((value, index) => (
          <button key={index} onClick={() => handleClick(index)}>
            {value}
          </button>
        ))}
      </div>
    </div>
  );
};

export default GameBoard;
