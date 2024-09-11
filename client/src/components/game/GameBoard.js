// // import React, { useState, useEffect } from 'react';
// // import API from '../../services/api';
// // import { useParams } from 'react-router-dom';

// // function GameBoard() {
// //   const { gridSize } = useParams();
// //   const [board, setBoard] = useState(Array(gridSize * gridSize).fill(null));

// //   const handleMove = async (index) => {
// //     // Call the Flask API to make a move and update the game state
// //   };

// //   return (
// //     <div>
// //       <h2>Tic Tac Toe - Grid Size: {gridSize}</h2>
// //       <div style={{ display: 'grid', gridTemplateColumns: `repeat(${gridSize}, 50px)` }}>
// //         {board.map((cell, index) => (
// //           <div
// //             key={index}
// //             style={{ width: 50, height: 50, border: '1px solid black', textAlign: 'center', lineHeight: '50px' }}
// //             onClick={() => handleMove(index)}
// //           >
// //             {cell}
// //           </div>
// //         ))}
// //       </div>
// //     </div>
// //   );
// // }

// // export default GameBoard;



// import React, { useEffect, useState } from 'react';
// import { useParams } from 'react-router-dom';
// import API from '../../services/api';

// const GameBoard = () => {
//     const { game_id } = useParams();
//     const [gameState, setGameState] = useState([]);
//     const [player, setPlayer] = useState('X'); // Set default player
//     const [error, setError] = useState(null);

//     useEffect(() => {
//         const fetchGameState = async () => {
//             try {
//                 const response = await API.get(`/game/${game_id}`);
//                 if (response.status === 200) {
//                     setGameState(response.data.game_state || []);
//                 }
//             } catch (error) {
//                 setError('Error fetching game state');
//             }
//         };

//         fetchGameState();
//     }, [game_id]);

//     const handleMove = async (position) => {
//         try {
//             const response = await API.post('/move', {
//                 game_id,
//                 player,
//                 position
//             });
//             if (response.status === 200) {
//                 setGameState(response.data.game_state);
//                 if (response.data.winner) {
//                     alert(`${response.data.winner} wins!`);
//                 } else if (response.data.result === 'draw') {
//                     alert('It\'s a draw!');
//                 }
//             }
//         } catch (error) {
//             setError('Error making move');
//         }
//     };

//     const renderCell = (index) => (
//         <div
//             key={index}
//             className={`cell ${gameState[index]}`}
//             onClick={() => handleMove(index)}
//         >
//             {gameState[index]}
//         </div>
//     );

//     const gridSize = Math.sqrt(gameState.length);

//     return (
//         <div>
//             <h2>Game Board</h2>
//             {error && <p>{error}</p>}
//             <div
//                 className="game-board"
//                 style={{
//                     gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
//                     gridTemplateRows: `repeat(${gridSize}, 1fr)`
//                 }}
//             >
//                 {gameState.map((_, index) => renderCell(index))}
//             </div>
//         </div>
//     );
// };

// export default GameBoard;


// src/components/game/GameBoard.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function GameBoard() {
    const { gridSize } = useParams();
    const [gameState, setGameState] = useState([]);
    const [currentPlayer, setCurrentPlayer] = useState('X'); // Example state
    const [winner, setWinner] = useState(null);

    useEffect(() => {
        // Initialize the game state when the component mounts
        const initGame = async () => {
            try {
                const response = await axios.post('/game', { grid_size: parseInt(gridSize), player_x: 1 });
                setGameState(response.data.game_state);
            } catch (err) {
                console.error(err);
            }
        };

        initGame();
    }, [gridSize]);

    const handleCellClick = async (index) => {
        if (gameState[index] || winner) return;

        try {
            const response = await axios.post('/move', {
                game_id: 1, // Provide the actual game ID
                player: currentPlayer,
                position: index,
            });

            setGameState(response.data.game_state);
            if (response.data.winner) {
                setWinner(response.data.winner);
            }
            setCurrentPlayer(currentPlayer === 'X' ? 'O' : 'X');
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div>
            <h2>Game Board ({gridSize}x{gridSize})</h2>
            <div style={{ display: 'grid', gridTemplateColumns: `repeat(${gridSize}, 50px)` }}>
                {gameState.map((cell, index) => (
                    <div
                        key={index}
                        onClick={() => handleCellClick(index)}
                        style={{ width: '50px', height: '50px', border: '1px solid black', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px' }}
                    >
                        {cell}
                    </div>
                ))}
            </div>
            {winner && <h3>Winner: {winner}</h3>}
        </div>
    );
}

export default GameBoard;

