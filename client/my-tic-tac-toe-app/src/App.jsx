import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import HomePage from './HomePage';
import GamePage from './GamePage';
import LoginComponent from './LoginComponent';
import RegisterComponent from './RegisterComponent';

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={HomePage} />
        <Route path="/game" component={GamePage} />
        <Route path="/login" component={LoginComponent} />
        <Route path="/register" component={RegisterComponent} />
      </Switch>
    </Router>
  );
};

export default App;

