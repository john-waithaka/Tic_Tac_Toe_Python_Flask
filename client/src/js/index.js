document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    // Get form values
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');
  
    // Simple validation
    if (!username || !password) {
      errorMessage.style.display = 'block';
    } else {
      errorMessage.style.display = 'none';
  
      // Simulate form submission to the server
      console.log('Form submitted:', { username, password });
  
      // In a real scenario, you'd submit to the Flask API endpoint for registration
      // e.g., fetch('/api/register', { method: 'POST', body: JSON.stringify({ username, password }) })
  
      alert('Registration successful! Redirecting to the game...');
      window.location.href = '/game';
    }
  });
  