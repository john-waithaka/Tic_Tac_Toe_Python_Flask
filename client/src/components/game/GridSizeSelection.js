// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';

// function GridSizeSelection() {
//   const [gridSize, setGridSize] = useState(3);
//   const navigate = useNavigate();

//   const handleStartGame = () => {
//     navigate(`/game/${gridSize}`);
//   };

//   return (
//     <div className="container">
//       <h1>Choose Grid Size</h1>
//       <input
//         type="number"
//         value={gridSize}
//         onChange={(e) => setGridSize(Math.max(3, Math.min(8, parseInt(e.target.value))))}
//         min="3"
//         max="8"
//       />
//       <button onClick={handleStartGame}>Start Game</button>
//     </div>
//   );
// }

// export default GridSizeSelection;



import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../../services/api';

const GridSizeSelection = () => {
    const [gridSize, setGridSize] = useState(3);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const playerId = localStorage.getItem('user_id'); // Assuming user ID is stored in local storage
        try {
            const response = await API.post('/game', { grid_size: gridSize, player_x: playerId });
            if (response.status === 201) {
                const { game_id } = response.data;
                navigate(`/game/${game_id}`);
            }
        } catch (error) {
            console.error("Error creating game:", error);
        }
    };

    return (
        <div>
            <h2>Select Grid Size</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Grid Size:
                    <select value={gridSize} onChange={(e) => setGridSize(parseInt(e.target.value, 10))}>
                        {[...Array(6).keys()].map(i => (
                            <option key={i + 3} value={i + 3}>
                                {i + 3} x {i + 3}
                            </option>
                        ))}
                    </select>
                </label>
                <button type="submit">Start Game</button>
            </form>
        </div>
    );
};

export default GridSizeSelection;
