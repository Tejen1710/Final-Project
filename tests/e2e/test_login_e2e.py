"""
Playwright E2E Tests for Login
Tests both positive and negative scenarios for user login
"""
import pytest
import random


class TestLogin:
    """Test suite for login page E2E tests"""
    
    def test_login_success_with_valid_credentials(self, page, base_url):
        """
        POSITIVE TEST: Login with valid email and password
        Verifies success message and token storage
        """
        # First, register a user
        unique_id = random.randint(10000, 99999)
        test_email = f"loginuser{unique_id}@example.com"
        test_password = "validPassword123"
        
        # Register the user
        page.goto(f"{base_url}/static/register.html")
        page.fill("#email", test_email)
        page.fill("#password", test_password)
        page.fill("#confirm-password", test_password)
        page.click("button[type='submit']")
        page.wait_for_timeout(1000)  # Wait for registration
        
        # Clear localStorage
        page.evaluate("() => localStorage.clear()")
        
        # Now go to login page
        page.goto(f"{base_url}/static/login.html")
        
        # Fill login form
        page.fill("#email", test_email)
        page.fill("#password", test_password)
        
        # Submit form
        page.click("button[type='submit']")
        
        # Wait for success message
        success_message = page.locator("#success")
        success_message.wait_for(state="visible", timeout=5000)
        
        # Verify success message
        assert "successful" in success_message.text_content().lower()
        
        # Verify no error message
        error_message = page.locator("#error")
        assert error_message.text_content() == ""
        
        # Verify JWT token is stored in localStorage
        token = page.evaluate("() => localStorage.getItem('token')")
        assert token is not None
        assert len(token) > 0
    
    def test_login_with_invalid_credentials_shows_error(self, page, base_url):
        """
        NEGATIVE TEST: Login with incorrect password
        Should show 401 Unauthorized error
        """
        page.goto(f"{base_url}/static/login.html")
        
        # Try to login with non-existent credentials
        page.fill("#email", "nonexistent@example.com")
        page.fill("#password", "wrongpassword123")
        
        # Submit form
        page.click("button[type='submit']")
        
        # Wait for error message
        error_message = page.locator("#error")
        error_message.wait_for(state="visible", timeout=3000)
        
        # Verify error message about invalid credentials
        error_text = error_message.text_content().lower()
        assert "invalid" in error_text or "credentials" in error_text or "incorrect" in error_text
        
        # Verify no success message
        success_message = page.locator("#success")
        assert success_message.text_content() == ""
        
        # Verify no token stored
        token = page.evaluate("() => localStorage.getItem('token')")
        assert token is None
    
    def test_login_with_wrong_password_shows_error(self, page, base_url):
        """
        NEGATIVE TEST: Login with correct email but wrong password
        Should show 401 error
        """
        # First register a user
        unique_id = random.randint(10000, 99999)
        test_email = f"wrongpass{unique_id}@example.com"
        test_password = "correctPassword123"
        
        page.goto(f"{base_url}/static/register.html")
        page.fill("#email", test_email)
        page.fill("#password", test_password)
        page.fill("#confirm-password", test_password)
        page.click("button[type='submit']")
        page.wait_for_timeout(1000)
        
        # Now try to login with wrong password
        page.goto(f"{base_url}/static/login.html")
        page.fill("#email", test_email)
        page.fill("#password", "wrongPassword456")
        page.click("button[type='submit']")
        
        # Wait for error message
        error_message = page.locator("#error")
        error_message.wait_for(state="visible", timeout=3000)
        
        # Verify error message
        error_text = error_message.text_content().lower()
        assert "invalid" in error_text or "credentials" in error_text
        
        # Verify no success message
        success_message = page.locator("#success")
        assert success_message.text_content() == ""
    
    def test_login_with_invalid_email_format_shows_error(self, page, base_url):
        """
        NEGATIVE TEST: Login with invalid email format
        Should show client-side validation error
        """
        page.goto(f"{base_url}/static/login.html")
        
        # Fill form with invalid email
        page.fill("#email", "notanemail")  # No @ symbol
        page.fill("#password", "password123")
        
        # Submit form
        page.click("button[type='submit']")
        
        # Wait for error message
        error_message = page.locator("#error")
        error_message.wait_for(state="visible", timeout=2000)
        
        # Verify error message about email format
        assert "email" in error_message.text_content().lower()
        
        # Verify no success message
        success_message = page.locator("#success")
        assert success_message.text_content() == ""
    
    def test_login_with_empty_password_shows_error(self, page, base_url):
        """
        NEGATIVE TEST: Login with empty password
        Should show client-side validation error
        """
        page.goto(f"{base_url}/static/login.html")
        
        # Fill only email, leave password empty
        page.fill("#email", "test@example.com")
        # Don't fill password
        
        # Submit form
        page.click("button[type='submit']")
        
        # Wait for error message
        error_message = page.locator("#error")
        error_message.wait_for(state="visible", timeout=2000)
        
        # Verify error message about password
        assert "password" in error_message.text_content().lower()
        
        # Verify no success message
        success_message = page.locator("#success")
        assert success_message.text_content() == ""
    
    def test_login_page_elements_present(self, page, base_url):
        """
        POSITIVE TEST: Verify all form elements are present
        """
        page.goto(f"{base_url}/static/login.html")
        
        # Check form elements exist
        assert page.locator("#email").is_visible()
        assert page.locator("#password").is_visible()
        assert page.locator("button[type='submit']").is_visible()
        
        # Check input types
        assert page.locator("#email").get_attribute("type") == "email"
        assert page.locator("#password").get_attribute("type") == "password"
    
    def test_full_workflow_register_then_login(self, page, base_url):
        """
        POSITIVE TEST: Complete workflow - register a new user, then login
        """
        # Generate unique credentials
        unique_id = random.randint(10000, 99999)
        test_email = f"workflow{unique_id}@example.com"
        test_password = "workflowPassword123"
        
        # Step 1: Register
        page.goto(f"{base_url}/static/register.html")
        page.fill("#email", test_email)
        page.fill("#password", test_password)
        page.fill("#confirm-password", test_password)
        page.click("button[type='submit']")
        
        # Verify registration success
        success_message = page.locator("#success")
        success_message.wait_for(state="visible", timeout=5000)
        assert "successful" in success_message.text_content().lower()
        
        # Clear the token
        page.evaluate("() => localStorage.clear()")
        
        # Step 2: Login with same credentials
        page.goto(f"{base_url}/static/login.html")
        page.fill("#email", test_email)
        page.fill("#password", test_password)
        page.click("button[type='submit']")
        
        # Verify login success
        success_message = page.locator("#success")
        success_message.wait_for(state="visible", timeout=5000)
        assert "successful" in success_message.text_content().lower()
        
        # Verify token exists
        token = page.evaluate("() => localStorage.getItem('token')")
        assert token is not None
        assert len(token) > 0
