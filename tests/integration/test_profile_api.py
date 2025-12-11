# tests/integration/test_profile_api.py
from app import crud, schemas, security


class TestProfileAPI:
    """Integration tests for user profile endpoints"""
    
    def test_get_profile_authenticated(self, client, db_session):
        """Test retrieving own profile with valid token"""
        # Create a test user
        user_create = schemas.UserCreate(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        user = crud.create_user(db_session, user_create)
        
        # Create JWT token
        token = security.create_access_token({"sub": user.email})
        
        # Get profile
        response = client.get(
            "/profile",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "id" in data
        assert "created_at" in data
    
    def test_get_profile_unauthenticated(self, client):
        """Test 401 error when no token provided"""
        response = client.get("/profile")
        assert response.status_code == 401  # HTTPBearer returns 401
    
    def test_get_profile_invalid_token(self, client):
        """Test 401 error with invalid token"""
        response = client.get(
            "/profile",
            headers={"Authorization": "Bearer invalid_token_here"}
        )
        assert response.status_code == 401
    
    def test_update_profile_success(self, client, db_session):
        """Test successful profile update with DB verification"""
        # Create user
        user_create = schemas.UserCreate(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        user = crud.create_user(db_session, user_create)
        token = security.create_access_token({"sub": user.email})
        
        # Update profile
        update_data = {
            "email": "newemail@example.com",
            "bio": "This is my new bio"
        }
        response = client.put(
            "/profile",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newemail@example.com"
        assert data["bio"] == "This is my new bio"
        assert data["profile_updated_at"] is not None
        
        # Verify in database
        db_session.refresh(user)
        updated_user = crud.get_user_by_id(db_session, user.id)
        assert updated_user.email == "newemail@example.com"
        assert updated_user.bio == "This is my new bio"
    
    def test_update_profile_bio_only(self, client, db_session):
        """Test updating only bio field"""
        user_create = schemas.UserCreate(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        user = crud.create_user(db_session, user_create)
        token = security.create_access_token({"sub": user.email})
        
        update_data = {"bio": "Just updating my bio"}
        response = client.put(
            "/profile",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["bio"] == "Just updating my bio"
        assert data["email"] == "test@example.com"  # Email unchanged
    
    def test_update_profile_email_already_taken(self, client, db_session):
        """Test error when trying to change to an existing email"""
        # Create two users
        crud.create_user(db_session, schemas.UserCreate(
            username="user1",
            email="user1@example.com",
            password="password123"
        ))
        user2 = crud.create_user(db_session, schemas.UserCreate(
            username="user2",
            email="user2@example.com",
            password="password123"
        ))
        
        # User2 tries to change email to user1's email
        token = security.create_access_token({"sub": user2.email})
        update_data = {"email": "user1@example.com"}
        
        response = client.put(
            "/profile",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400
        assert "already in use" in response.json()["detail"].lower()
    
    def test_change_password_success(self, client, db_session):
        """Test successful password change and verify new password works"""
        # Create user
        user_create = schemas.UserCreate(
            username="testuser",
            email="test@example.com",
            password="oldpassword123"
        )
        user = crud.create_user(db_session, user_create)
        token = security.create_access_token({"sub": user.email})
        
        # Change password
        pwd_data = {
            "current_password": "oldpassword123",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }
        response = client.post(
            "/change-password",
            json=pwd_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert "success" in response.json()["message"].lower()
        
        # Verify old password no longer works
        db_session.refresh(user)
        assert not security.verify_password("oldpassword123", user.password_hash)
        
        # Verify new password works
        assert security.verify_password("newpassword123", user.password_hash)
        
        # Verify can login with new password
        login_response = client.post(
            "/login",
            json={"email": "test@example.com", "password": "newpassword123"}
        )
        assert login_response.status_code == 200
    
    def test_change_password_wrong_current(self, client, db_session):
        """Test error when current password is incorrect"""
        user_create = schemas.UserCreate(
            username="testuser",
            email="test@example.com",
            password="correctpassword"
        )
        user = crud.create_user(db_session, user_create)
        token = security.create_access_token({"sub": user.email})
        
        pwd_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }
        response = client.post(
            "/change-password",
            json=pwd_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_change_password_mismatch(self, client, db_session):
        """Test error when new passwords don't match"""
        user_create = schemas.UserCreate(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        user = crud.create_user(db_session, user_create)
        token = security.create_access_token({"sub": user.email})
        
        pwd_data = {
            "current_password": "password123",
            "new_password": "newpassword123",
            "confirm_password": "differentpassword"
        }
        response = client.post(
            "/change-password",
            json=pwd_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_change_password_too_short(self, client, db_session):
        """Test error when new password is too short"""
        user_create = schemas.UserCreate(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        user = crud.create_user(db_session, user_create)
        token = security.create_access_token({"sub": user.email})
        
        pwd_data = {
            "current_password": "password123",
            "new_password": "short",  # Less than 8 characters
            "confirm_password": "short"
        }
        response = client.post(
            "/change-password",
            json=pwd_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_profile_unauthenticated(self, client):
        """Test that profile endpoints require authentication"""
        # Try to update profile without token
        response = client.put("/profile", json={"bio": "test"})
        assert response.status_code == 401
        
        # Try to change password without token
        response = client.post("/change-password", json={
            "current_password": "old",
            "new_password": "newpass123",
            "confirm_password": "newpass123"
        })
        assert response.status_code == 401
