# tests/e2e/test_profile_e2e.py
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def register_and_login(page: Page, base_url):
    """Helper fixture to register a new user and login"""
    # Generate unique email
    import time
    email = f"testuser{int(time.time())}@example.com"
    password = "password123"
    
    # Navigate to register page
    page.goto(f"{base_url}/static/register.html")
    page.wait_for_load_state("networkidle")
    
    # Register
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    
    # Wait for redirect or success
    page.wait_for_timeout(1000)
    
    return {"email": email, "password": password}


class TestProfileE2E:
    """End-to-end tests for user profile workflow"""
    
    def test_profile_view_workflow(self, page: Page, base_url, server, register_and_login):
        """Test full workflow: login → view profile → check data displayed"""
        credentials = register_and_login
        
        # Navigate to profile page
        page.goto(f"{base_url}/static/profile.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Check that profile data is loaded
        username_elem = page.locator("#displayUsername")
        email_elem = page.locator("#displayEmail")
        
        # Wait for content to load
        expect(username_elem).not_to_be_empty(timeout=5000)
        expect(email_elem).to_contain_text(credentials["email"], timeout=5000)
        
        # Verify form fields are populated
        email_input = page.locator("#email")
        expect(email_input).to_have_value(credentials["email"])
    
    def test_profile_update_workflow(self, page: Page, base_url, server, register_and_login):
        """Test full workflow: login → update profile → verify changes"""
        register_and_login  # Use fixture to authenticate
        
        # Navigate to profile page
        page.goto(f"{base_url}/static/profile.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Update bio
        new_bio = "This is my updated bio for E2E testing"
        page.fill("#bio", new_bio)
        
        # Submit profile form
        page.click("#profileForm button[type='submit']")
        
        # Wait for success message
        page.wait_for_timeout(1500)
        
        # Check for success alert
        alert = page.locator("#alertBox")
        expect(alert).to_contain_text("success", timeout=5000)
        
        # Reload page and verify bio persists
        page.reload()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        bio_input = page.locator("#bio")
        expect(bio_input).to_have_value(new_bio, timeout=5000)
    
    def test_password_change_workflow(self, page: Page, base_url, server, register_and_login):
        """Test full workflow: login → change password → logout → login with new password"""
        credentials = register_and_login
        old_password = credentials["password"]
        new_password = "newpassword456"
        
        # Navigate to profile page
        page.goto(f"{base_url}/static/profile.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Fill password change form
        page.fill("#currentPassword", old_password)
        page.fill("#newPassword", new_password)
        page.fill("#confirmPassword", new_password)
        
        # Submit password change form
        page.click("#passwordForm button[type='submit']")
        
        # Wait for success message and redirect
        page.wait_for_timeout(3000)
        
        # Should be redirected to login page
        expect(page).to_have_url(f"{base_url}/static/login.html", timeout=5000)
        
        # Try to login with new password
        page.fill('input[name="email"]', credentials["email"])
        page.fill('input[name="password"]', new_password)
        page.click('button[type="submit"]')
        
        # Wait for successful login (redirect to calculations page)
        page.wait_for_timeout(2000)
        
        # Verify we're logged in (should redirect to calculations or show success)
        # Check URL changed or token exists
        token = page.evaluate("() => localStorage.getItem('token')")
        assert token is not None, "Should have JWT token after login"
    
    def test_password_change_wrong_current_password(self, page: Page, base_url, server, register_and_login):
        """Test error handling when current password is wrong"""
        register_and_login  # Use fixture to authenticate
        
        # Navigate to profile page
        page.goto(f"{base_url}/static/profile.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Fill password change form with wrong current password
        page.fill("#currentPassword", "wrongpassword")
        page.fill("#newPassword", "newpassword456")
        page.fill("#confirmPassword", "newpassword456")
        
        # Submit password change form
        page.click("#passwordForm button[type='submit']")
        
        # Wait for error message
        page.wait_for_timeout(1500)
        
        # Check for error alert
        alert = page.locator("#alertBox")
        expect(alert).to_contain_text("incorrect", timeout=5000)
    
    def test_password_change_mismatch_validation(self, page: Page, base_url, server, register_and_login):
        """Test client-side validation when passwords don't match"""
        credentials = register_and_login
        
        # Navigate to profile page
        page.goto(f"{base_url}/static/profile.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Fill password change form with mismatched passwords
        page.fill("#currentPassword", credentials["password"])
        page.fill("#newPassword", "newpassword456")
        page.fill("#confirmPassword", "differentpassword")
        
        # Submit password change form
        page.click("#passwordForm button[type='submit']")
        
        # Wait for validation message
        page.wait_for_timeout(1000)
        
        # Check for validation error
        alert = page.locator("#alertBox")
        expect(alert).to_contain_text("match", timeout=5000)
    
    def test_profile_navigation_links(self, page: Page, base_url, server, register_and_login):
        """Test navigation from profile to calculations page"""
        register_and_login  # Use fixture to authenticate
        
        # Navigate to profile page
        page.goto(f"{base_url}/static/profile.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Click on "My Calculations" link
        page.click('a[href="/static/calculations.html"]')
        page.wait_for_timeout(1000)
        
        # Verify we're on calculations page
        expect(page).to_have_url(f"{base_url}/static/calculations.html", timeout=5000)
    
    def test_profile_logout(self, page: Page, base_url, server, register_and_login):
        """Test logout functionality from profile page"""
        register_and_login  # Use fixture to authenticate
        
        # Navigate to profile page
        page.goto(f"{base_url}/static/profile.html")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # Click logout
        page.click("#logoutLink")
        page.wait_for_timeout(1000)
        
        # Verify redirected to login and token cleared
        expect(page).to_have_url(f"{base_url}/static/login.html", timeout=5000)
        token = page.evaluate("() => localStorage.getItem('token')")
        assert token is None, "Token should be cleared after logout"
    
    def test_profile_unauthorized_access(self, page: Page, base_url, server):
        """Test that unauthenticated users are redirected from profile page"""
        # Clear any existing tokens
        page.goto(f"{base_url}/static/login.html")
        page.evaluate("() => localStorage.removeItem('token')")
        
        # Try to access profile page without login
        page.goto(f"{base_url}/static/profile.html")
        page.wait_for_timeout(1500)
        
        # Should be redirected to login page
        expect(page).to_have_url(f"{base_url}/static/login.html", timeout=5000)
