// profile.js - User Profile Management

const API_BASE_URL = '';

// Show alert message
function showAlert(message, type = 'success') {
    const alertBox = document.getElementById('alertBox');
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
    alertBox.style.display = 'block';
    
    setTimeout(() => {
        alertBox.style.display = 'none';
    }, 5000);
}

// Get token from localStorage
function getToken() {
    return localStorage.getItem('token');
}

// Check if user is authenticated
function checkAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = '/static/login.html';
        return false;
    }
    return true;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
}

// Calculate password strength
function calculatePasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    
    return Math.min(strength, 3); // 0=weak, 1=weak, 2=medium, 3=strong
}

// Update password strength indicator
function updatePasswordStrength(password) {
    const strengthBar = document.getElementById('strengthBar');
    const strengthContainer = document.getElementById('passwordStrength');
    
    if (password.length === 0) {
        strengthContainer.style.display = 'none';
        return;
    }
    
    strengthContainer.style.display = 'block';
    const strength = calculatePasswordStrength(password);
    
    strengthBar.className = 'password-strength-bar';
    
    if (strength <= 1) {
        strengthBar.classList.add('strength-weak');
    } else if (strength === 2) {
        strengthBar.classList.add('strength-medium');
    } else {
        strengthBar.classList.add('strength-strong');
    }
}

// Generate avatar initials
function generateAvatar(username) {
    const initials = username.substring(0, 2).toUpperCase();
    document.getElementById('avatarInitials').textContent = initials;
    document.getElementById('headerUsername').textContent = username;
}

// Load user calculations count
async function loadCalculationsCount() {
    const token = getToken();
    
    try {
        const response = await fetch(`${API_BASE_URL}/calculations/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const calculations = await response.json();
            document.getElementById('calcCount').textContent = calculations.length;
        }
    } catch (error) {
        console.error('Error loading calculations:', error);
    }
}

// Calculate days since registration
function calculateMemberDays(createdAt) {
    const created = new Date(createdAt);
    const now = new Date();
    const diffTime = Math.abs(now - created);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}

// Load user profile
async function loadProfile() {
    const token = getToken();
    
    try {
        const response = await fetch(`${API_BASE_URL}/profile`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/static/login.html';
            return;
        }
        
        if (!response.ok) {
            throw new Error('Failed to load profile');
        }
        
        const profile = await response.json();
        
        // Generate avatar with initials
        generateAvatar(profile.username);
        
        // Update display fields
        document.getElementById('displayUsername').textContent = profile.username;
        document.getElementById('displayEmail').textContent = profile.email;
        document.getElementById('displayCreatedAt').textContent = formatDate(profile.created_at);
        
        // Show last update if available
        if (profile.profile_updated_at) {
            document.getElementById('lastUpdateRow').style.display = 'flex';
            document.getElementById('displayLastUpdate').textContent = formatDate(profile.profile_updated_at);
            document.getElementById('profileUpdates').textContent = '1+';
        }
        
        // Calculate member days
        const memberDays = calculateMemberDays(profile.created_at);
        document.getElementById('memberDays').textContent = memberDays;
        
        // Update form fields
        document.getElementById('email').value = profile.email;
        document.getElementById('bio').value = profile.bio || '';
        
        // Load calculations count
        await loadCalculationsCount();
        
    } catch (error) {
        console.error('Error loading profile:', error);
        showAlert('Failed to load profile data', 'error');
    }
}

// Update profile
document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const token = getToken();
    const email = document.getElementById('email').value.trim();
    const bio = document.getElementById('bio').value.trim();
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showAlert('Please enter a valid email address', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/profile`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                bio: bio || null
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            // Handle specific error messages
            if (response.status === 400 && data.detail) {
                if (data.detail.toLowerCase().includes('already')) {
                    showAlert('This email is already in use by another account', 'error');
                } else {
                    showAlert(data.detail, 'error');
                }
            } else {
                showAlert(data.detail || 'Failed to update profile', 'error');
            }
            return;
        }
        
        // Update display fields with new data
        document.getElementById('displayEmail').textContent = data.email;
        
        showAlert('Profile updated successfully!', 'success');
        
        // Reload profile to get updated data
        await loadProfile();
        
    } catch (error) {
        console.error('Error updating profile:', error);
        showAlert('Network error. Please check your connection and try again.', 'error');
    }
});

// Change password
document.getElementById('passwordForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const token = getToken();
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // Client-side validation
    if (!currentPassword) {
        showAlert('Please enter your current password', 'error');
        return;
    }
    
    if (newPassword.length < 8) {
        showAlert('New password must be at least 8 characters long', 'error');
        return;
    }
    
    if (newPassword !== confirmPassword) {
        showAlert('New password and confirmation password do not match', 'error');
        return;
    }
    
    if (currentPassword === newPassword) {
        showAlert('New password must be different from current password', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/change-password`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword,
                confirm_password: confirmPassword
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            // Handle specific error messages
            if (response.status === 400 && data.detail) {
                if (data.detail.toLowerCase().includes('incorrect')) {
                    showAlert('Current password is incorrect', 'error');
                } else if (data.detail.toLowerCase().includes('match')) {
                    showAlert('New password and confirmation password do not match', 'error');
                } else {
                    showAlert(data.detail, 'error');
                }
            } else if (response.status === 422) {
                showAlert('Password validation failed. Please check your inputs.', 'error');
            } else {
                showAlert(data.detail || 'Failed to change password', 'error');
            }
            return;
        }
        
        showAlert('Password changed successfully! Redirecting to login...', 'success');
        
        // Clear form
        document.getElementById('passwordForm').reset();
        
        // Redirect to login after 2 seconds
        setTimeout(() => {
            localStorage.removeItem('token');
            window.location.href = '/static/login.html';
        }, 2000);
        
    } catch (error) {
        console.error('Error changing password:', error);
        showAlert('Network error. Please check your connection and try again.', 'error');
    }
});

// Add password strength indicator event listener
document.getElementById('newPassword').addEventListener('input', (e) => {
    updatePasswordStrength(e.target.value);
});

// Logout
document.getElementById('logoutLink').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.removeItem('token');
    window.location.href = '/static/login.html';
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    if (checkAuth()) {
        loadProfile();
    }
});
