console.log('login-error.js loaded');

document.addEventListener('DOMContentLoaded', function() {
    const hasError = window.location.search.includes('error') ||
        (document.querySelector('[data-django-messages]') && document.querySelector('[data-django-messages]').textContent.includes('Invalid'));
    console.log('hasError:', hasError);
    if (hasError) {
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const loginError = document.getElementById('loginErr');

        console.log('Showing login error message');
        // Apply red border
        usernameInput.style.borderColor = '#ef4444';
        passwordInput.style.borderColor = '#ef4444';

        // Show error message by removing hidden class and setting display block
        loginError.classList.remove('hidden');
        loginError.style.display = 'block';

        // Clear errors on input
        function clearError() {
            usernameInput.style.borderColor = '';
            passwordInput.style.borderColor = '';
            loginError.classList.add('hidden');
            loginError.style.display = 'none';
        }

        usernameInput.addEventListener('input', clearError);
        passwordInput.addEventListener('input', clearError);
    } else {
        console.log('No login error detected');
    }
});
