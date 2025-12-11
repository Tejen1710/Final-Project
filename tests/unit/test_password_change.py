# tests/unit/test_password_change.py
import pytest
from pydantic import ValidationError
from app import security
from app.schemas.user import PasswordChange, UserProfileUpdate


class TestPasswordHashing:
    """Unit tests for password hashing and verification"""
    
    def test_hash_password_creates_hash(self):
        """Test that hashing creates a different string"""
        password = "mypassword123"
        hashed = security.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert isinstance(hashed, str)
    
    def test_verify_password_success(self):
        """Test password verification with correct password"""
        password = "mypassword123"
        hashed = security.hash_password(password)
        
        assert security.verify_password(password, hashed) is True
    
    def test_verify_password_failure(self):
        """Test password verification with wrong password"""
        password = "mypassword123"
        wrong_password = "wrongpassword"
        hashed = security.hash_password(password)
        
        assert security.verify_password(wrong_password, hashed) is False
    
    def test_different_hashes_for_same_password(self):
        """Test that same password creates different hashes (due to salt)"""
        password = "mypassword123"
        hash1 = security.hash_password(password)
        hash2 = security.hash_password(password)
        
        # Hashes should be different due to different salts
        assert hash1 != hash2
        # But both should verify correctly
        assert security.verify_password(password, hash1)
        assert security.verify_password(password, hash2)


class TestPasswordChangeSchema:
    """Unit tests for PasswordChange Pydantic schema validation"""
    
    def test_password_change_valid(self):
        """Test valid password change data"""
        data = {
            "current_password": "oldpass123",
            "new_password": "newpass123",
            "confirm_password": "newpass123"
        }
        pwd_change = PasswordChange(**data)
        
        assert pwd_change.current_password == "oldpass123"
        assert pwd_change.new_password == "newpass123"
        assert pwd_change.confirm_password == "newpass123"
    
    def test_password_mismatch_validation(self):
        """Test validation fails when passwords don't match"""
        data = {
            "current_password": "oldpass123",
            "new_password": "newpass123",
            "confirm_password": "different123"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PasswordChange(**data)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
        assert any("password" in str(error).lower() for error in errors)
    
    def test_password_too_short(self):
        """Test validation fails when password is too short"""
        data = {
            "current_password": "oldpass123",
            "new_password": "short",  # Less than 8 characters
            "confirm_password": "short"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            PasswordChange(**data)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
    
    def test_password_minimum_length(self):
        """Test password with exactly 8 characters is valid"""
        data = {
            "current_password": "oldpass123",
            "new_password": "12345678",  # Exactly 8 characters
            "confirm_password": "12345678"
        }
        pwd_change = PasswordChange(**data)
        assert pwd_change.new_password == "12345678"


class TestUserProfileUpdateSchema:
    """Unit tests for UserProfileUpdate Pydantic schema"""
    
    def test_profile_update_valid_email(self):
        """Test valid email update"""
        data = {"email": "newemail@example.com"}
        profile_update = UserProfileUpdate(**data)
        
        assert profile_update.email == "newemail@example.com"
        assert profile_update.bio is None
    
    def test_profile_update_valid_bio(self):
        """Test valid bio update"""
        data = {"bio": "This is my new bio"}
        profile_update = UserProfileUpdate(**data)
        
        assert profile_update.bio == "This is my new bio"
        assert profile_update.email is None
    
    def test_profile_update_both_fields(self):
        """Test updating both email and bio"""
        data = {
            "email": "newemail@example.com",
            "bio": "New bio text"
        }
        profile_update = UserProfileUpdate(**data)
        
        assert profile_update.email == "newemail@example.com"
        assert profile_update.bio == "New bio text"
    
    def test_profile_update_invalid_email(self):
        """Test validation fails with invalid email"""
        data = {"email": "not-an-email"}
        
        with pytest.raises(ValidationError) as exc_info:
            UserProfileUpdate(**data)
        
        errors = exc_info.value.errors()
        assert len(errors) > 0
    
    def test_profile_update_empty_allowed(self):
        """Test that empty update is allowed (all fields optional)"""
        data = {}
        profile_update = UserProfileUpdate(**data)
        
        assert profile_update.email is None
        assert profile_update.bio is None
    
    def test_profile_update_none_bio(self):
        """Test that None bio is acceptable"""
        data = {"bio": None}
        profile_update = UserProfileUpdate(**data)
        
        assert profile_update.bio is None
