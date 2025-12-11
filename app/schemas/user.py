from pydantic import BaseModel, EmailStr, constr, ConfigDict, model_validator
from datetime import datetime

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8)

class UserRegister(BaseModel):
    """Schema for JWT-based registration (email + password only)"""
    email: EmailStr
    password: constr(min_length=8)

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    """Login schema that accepts either username or email"""
    username: str | None = None
    email: str | None = None  # Allow any string format here, let API validate
    password: str
    
    @model_validator(mode='after')
    def at_least_one_provided(self):
        """Ensure at least one of username or email is provided"""
        if not self.username and not self.email:
            raise ValueError('Either username or email must be provided')
        return self


class UserProfile(BaseModel):
    """Schema for user profile data"""
    id: int
    username: str
    email: EmailStr
    bio: str | None = None
    created_at: datetime
    profile_updated_at: datetime | None = None
    
    model_config = ConfigDict(from_attributes=True)


class UserProfileUpdate(BaseModel):
    """Schema for updating profile"""
    bio: str | None = None
    email: EmailStr | None = None


class PasswordChange(BaseModel):
    """Schema for password change"""
    current_password: str
    new_password: constr(min_length=8)
    confirm_password: str
    
    @model_validator(mode='after')
    def passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError('New password and confirmation do not match')
        return self
