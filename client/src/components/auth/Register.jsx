// // import React, { useState } from 'react';
// // import API from '../../services/api';

// // function Register() {
// //   const [email, setEmail] = useState('');
// //   const [password, setPassword] = useState('');

// //   const handleSubmit = async (e) => {
// //     e.preventDefault();
// //     try {
// //       await API.post('/register', { email, password });
// //       // Redirect to login page after successful registration
// //     } catch (error) {
// //       console.error('Registration error:', error);
// //     }
// //   };

// //   return (
// //     <form onSubmit={handleSubmit}>
// //       <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
// //       <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
// //       <button type="submit">Register</button>
// //     </form>
// //   );
// // }

// // export default Register;



// // src/components/auth/Register.jsx
// import React, { useState } from 'react';
// import API from '../../services/api';

// function Register() {
//   const [username, setUsername] = useState('');
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [error, setError] = useState('');

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await API.post('/register', { username, email, password });
//       alert(response.data.message);
//       window.location.href = '/login'; // Redirect after successful registration
//     } catch (err) {
//       setError(err.response?.data?.message || 'Registration failed');
//     }
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <label>
//         Username:
//         <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
//       </label>
//       <label>
//         Email:
//         <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
//       </label>
//       <label>
//         Password:
//         <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
//       </label>
//       <button type="submit">Register</button>
//       {error && <p>{error}</p>}
//     </form>
//   );
// }

// export default Register;



// src/components/game/GridSizeSelection.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

function GridSizeSelection() {
    const navigate = useNavigate();

    const handleGridSizeSelection = (size) => {
        navigate(`/game/${size}`);
    };

    return (
        <div>
            <h2>Select Grid Size</h2>
            <button onClick={() => handleGridSizeSelection(3)}>3x3</button>
            <button onClick={() => handleGridSizeSelection(4)}>4x4</button>
            <button onClick={() => handleGridSizeSelection(5)}>5x5</button>
            {/* Add more grid sizes if needed */}
        </div>
    );
}

export default GridSizeSelection;
