// Simple authentication system (client-side for demo)
// In production, use proper backend authentication

function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const remember = document.getElementById('remember')?.checked;
    
    // Demo authentication
    if (email && password) {
        const user = {
            email: email,
            name: email.split('@')[0],
            loginTime: new Date().toISOString()
        };
        
        if (remember) {
            localStorage.setItem('krishishakti_user', JSON.stringify(user));
        } else {
            sessionStorage.setItem('krishishakti_user', JSON.stringify(user));
        }
        
        showSuccess('Login successful! Redirecting...');
        setTimeout(() => {
            window.location.href = '/dashboard.html';
        }, 1000);
    }
}

function handleSignup(event) {
    event.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        showError('Passwords do not match!');
        return;
    }
    
    if (password.length < 8) {
        showError('Password must be at least 8 characters!');
        return;
    }
    
    const user = {
        name: name,
        email: email,
        signupTime: new Date().toISOString()
    };
    
    localStorage.setItem('airwater_user', JSON.stringify(user));
    
    showSuccess('Account created! Redirecting...');
    setTimeout(() => {
        window.location.href = '/dashboard.html';
    }, 1000);
}

function demoLogin() {
    const demoUser = {
        email: 'demo@airwater.pro',
        name: 'Demo User',
        loginTime: new Date().toISOString()
    };
    
    sessionStorage.setItem('airwater_user', JSON.stringify(demoUser));
    
    showSuccess('Demo login successful! Redirecting...');
    setTimeout(() => {
        window.location.href = '/dashboard.html';
    }, 1000);
}

function showSuccess(message) {
    const alert = document.createElement('div');
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    alert.textContent = message;
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 3000);
}

function showError(message) {
    const alert = document.createElement('div');
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ef4444;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    alert.textContent = message;
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 3000);
}
