document.addEventListener['DOMContentLoaded',function () {
    const hasError = window.location.search.includes('error')||
                    document.querySelector('[data-django-messages]')?.textContent.includes('Invalid');
    if (hasError){
        const usernameInput = document.getElementById('username');
        const paswordInput = document.getElementById('password');
        const loginErr = document.getElementById('loginErr');
        
        //Apply red boarder
        usernameInput.style.boarderColor = '#ef4444';
        paswordInput.style.boarderColor = '#ef4444';

        //Err message
        loginErr.classList.remove('hidden');

        //clear Err on input
        function clearError(){
            usernameInput.style.boarderColor = '';
            passwordInput.style.boarderColor = '';
            loginErr.classList.add = 'hidden';
        }

        usernameInput.addEventListener('input', clearError)
        passwordInput.addEventListener('input', clearError)
    }
}]