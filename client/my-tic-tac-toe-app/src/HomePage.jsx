import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div>
      <h1>Welcome to Tic-Tac-Toe</h1>
      <nav>
        <Link to="/game">Start Game</Link>
        <br />
        <Link to="/login">Login</Link>
        <br />
        <Link to="/register">Register</Link>
      </nav>
    </div>
  );
};

export default HomePage;
