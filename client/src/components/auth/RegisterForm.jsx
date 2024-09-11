import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../../services/api'; // Import your Axios API

function RegisterForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate(); // To redirect after successful registration

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!username || !password) {
      setErrorMessage('Please fill out all fields.');
      return;
    }

    try {
      const response = await API.post('/register', { username, password });
      console.log('Registration successful:', response);
      alert('Registration successful! Redirecting to the login page...');
      navigate('/login'); // Redirect to login page after successful registration
    } catch (error) {
      console.error('Registration error:', error);
      setErrorMessage('Registration failed. Please try again.');
    }
  };

  return (
    <div className="container">
      <h1>Register</h1>
      <form id="registrationForm" onSubmit={handleSubmit}>
        <label htmlFor="username">Username</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter your username"
          required
        />

        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
          required
        />

        <button type="submit">Register</button>

        {errorMessage && <p className="message">{errorMessage}</p>}
      </form>

      <div className="login-redirect">
        <p>Already registered? <a href="/login">Click here to log in</a></p>
      </div>
    </div>
  );
}

export default RegisterForm;
