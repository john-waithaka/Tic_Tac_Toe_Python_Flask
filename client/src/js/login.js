document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    // Get form values
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const errorMessage = document.getElementById('login-error-message');

    // Simple validation
    if (!username || !password) {
        errorMessage.style.display = 'block';
        return;
    }

    // Submit login request
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            alert('Login successful! Redirecting to the game...');
            window.location.href = '/game_play.html';
        } else {
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        console.error('Error during login:', error);
    }
});
