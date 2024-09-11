// set up Axios for making HTTP requests to your Flask backend:

// import axios from 'axios';

// const API = axios.create({
//   baseURL: 'http://localhost:5000', // Adjust this to match your Flask backend
// });

// // Automatically add JWT token to every request
// API.interceptors.request.use((req) => {
//   const token = localStorage.getItem('token');
//   if (token) {
//     req.headers.Authorization = `Bearer ${token}`;
//   }
//   return req;
// });

// export default API;



// src/services/api.jsx
import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL, // Use environment variable
});

// Automatically add JWT token to every request
API.interceptors.request.use((req) => {
  const token = localStorage.getItem('token');
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

export default API;
