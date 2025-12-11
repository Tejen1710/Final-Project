# FastAPI Calculator with BREAD Operations - Final Project

## Overview
This is a **Final Project** for IS601 that implements complete BREAD (Browse, Read, Edit, Add, Delete) functionality for calculations with JWT authentication, comprehensive front-end interface, Playwright E2E tests, and automated CI/CD deployment to Docker Hub.

## Key Features
- **Complete BREAD Operations**: Browse, Read, Edit, Add, Delete calculations with user authentication
- **JWT Authentication**: Secure token-based authentication protecting all calculation endpoints
- **Interactive Front-End**: Comprehensive calculations manager with tabbed interface for all operations
- **User-Specific Data**: Each user can only view and manage their own calculations
- **User Management**: Registration, login with secure password hashing (PBKDF2-SHA256)
- **Calculation Types**: Add, Subtract, Multiply, Divide with automatic result computation
- **Data Validation**: Client-side and server-side validation (divide-by-zero, numeric checks)
- **Database Integration**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **Comprehensive E2E Testing**: Playwright tests for all BREAD operations (positive & negative scenarios)
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **CI/CD Pipeline**: GitHub Actions with automated testing and Docker Hub deployment
- **Docker Support**: Containerized deployment ready

## 🆕 Project Features
- **Authenticated BREAD Endpoints**: All calculation operations require JWT authentication
- **User-Scoped Calculations**: Users can only access their own calculation data
- **Complete Frontend Interface**: Full-featured calculations manager with Browse, Add, Edit operations
- **Enhanced E2E Tests**: Comprehensive Playwright tests covering all BREAD scenarios
- **Automated CI/CD**: GitHub Actions pipeline with automated testing and Docker Hub deployment

## 🎓 Final Project Feature: User Profile & Password Management

### New Features
This Final Project adds comprehensive user profile management capabilities with a modern, visually appealing interface:

#### Core Functionality
- **User Profile Management**: View and update user profile information (email, bio)
- **Password Change**: Securely change password with current password verification
- **Profile Page**: Dedicated profile page at `/static/profile.html` with modern purple gradient UI
- **Profile Fields**: Users can add a bio/about section (500 characters) to personalize their profile
- **Security**: All profile operations require JWT authentication
- **Timestamp Tracking**: Profile updates are tracked with `profile_updated_at` field

#### UI/UX Enhancements (Impressive Features! 🌟)
- **Modern Gradient Design**: Eye-catching purple/pink gradient background with glassmorphism effects
- **Avatar with Initials**: Dynamic avatar circle displaying user's initials at the top
- **Profile Statistics Dashboard**: Real-time stats showing:
  - Total calculations count
  - Days since account creation (member days)
  - Profile update count
- **Password Strength Indicator**: Real-time visual feedback with color-coded strength meter:
  - Red = Weak (< 8 chars or simple)
  - Orange = Medium (good length + some complexity)
  - Green = Strong (12+ chars with uppercase, lowercase, numbers, special chars)
- **Smooth Animations**: 
  - Slide-in effect on page load
  - Card hover effects with elevation changes
  - Animated alerts and transitions
- **Professional Color Scheme**: Purple (#667eea), Pink (#f5576c) gradients with white cards
- **Enhanced User Info Card**: Gradient card with emoji icons for better visual hierarchy
- **Responsive Design**: Mobile-friendly with proper scaling on all devices
- **Error Handling**: User-friendly error messages with specific feedback (duplicate email, password mismatch, etc.)

### New API Endpoints

| Method | Endpoint | Description | Request Body | Response | Auth Required |
|--------|----------|-------------|--------------|----------|---------------|
| GET | `/profile` | Get current user profile | - | `UserProfile` (200) | Yes |
| PUT | `/profile` | Update profile (email, bio) | `UserProfileUpdate` | `UserProfile` (200) | Yes |
| POST | `/change-password` | Change password | `PasswordChange` | `{message}` (200) | Yes |

### Technical Implementation Highlights

#### Backend Architecture
- **RESTful API Design**: Three new authenticated endpoints following REST principles
- **Database Schema Extension**: Added `bio` (VARCHAR 500) and `profile_updated_at` (TIMESTAMP) columns
- **Data Validation**: Multi-layer validation (Pydantic schemas, database constraints, business logic)
- **Email Uniqueness Check**: Prevents duplicate emails across user updates
- **Password Security**: Current password verification before allowing changes
- **Automatic Timestamps**: Updates `profile_updated_at` on every profile modification

#### Frontend Features
- **Single Page Application (SPA) Pattern**: Dynamic content loading without page refreshes
- **Fetch API Integration**: Modern async/await JavaScript for API communication
- **Local Storage JWT**: Secure token storage and automatic authentication
- **Real-time Calculations**: Fetches user's calculation count from API
- **Date Calculations**: Client-side computation of membership duration
- **Form Validation**: Client-side checks before API calls to reduce server load
- **Password Strength Algorithm**: Multi-factor strength calculation (length, complexity, character variety)

### Profile Schemas

- **UserProfile**: `{id, username, email, bio, created_at, profile_updated_at}` - Full profile data
- **UserProfileUpdate**: `{email?, bio?}` - Optional fields for profile updates
- **PasswordChange**: `{current_password, new_password, confirm_password}` - Password change validation with @model_validator

### User Workflows

1. **View Profile**: Login → Navigate to `/static/profile.html` → View profile information
2. **Update Profile**: Login → Profile page → Update email/bio → Submit → See success message
3. **Change Password**: Login → Profile page → Enter current & new password → Submit → Auto-logout → Re-login with new password
4. **Profile Navigation**: Access calculations from profile page or logout securely

## Project Structure

```
app/
├── __init__.py              # App initialization
├── main.py                  # FastAPI application & routes
├── database.py              # Database configuration & session management
├── crud.py                  # Database operations (Create, Read, Update, Delete)
├── security.py              # Password hashing and verification
├── models.py                # Wrapper for models package
├── schemas.py               # Wrapper for schemas package
├── models/
│   ├── __init__.py
│   ├── user.py              # User database model
│   └── calculation.py       # Calculation database model
├── schemas/
│   ├── __init__.py
│   ├── user.py              # User Pydantic schemas (UserCreate, UserRead, UserLogin)
│   └── calculation.py       # Calculation Pydantic schemas (CalculationCreate, CalculationRead, CalculationUpdate, CalcType)
└── services/
    ├── __init__.py
    └── factory.py           # Calculation factory pattern implementation

tests/
├── __init__.py
├── conftest.py              # Pytest configuration & shared fixtures
├── test_security.py         # Password hashing/verification tests
├── test_schemas.py          # Pydantic schema validation tests
├── test_users_api.py        # User API endpoint tests
├── unit/
│   ├── test_calculation_factory.py   # Factory pattern unit tests
│   └── test_calculation_schema.py    # Calculation schema validation tests
└── integration/
    ├── test_calculation_db.py        # Calculation database integration tests
    └── test_users_calculations_api.py # Complete API endpoint integration tests (28 tests)

Root Files:
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup for local development
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── reflection.md           # Project reflection notes
```

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Request Body | Response | Auth Required |
|--------|----------|-------------|--------------|----------|---------------|
| POST | `/register` | Register new user | `{email, password}` | `Token` (201) | No |
| POST | `/login` | Authenticate user | `{email, password}` | `Token` (200) | No |

### User Endpoints (Legacy Compatibility)

| Method | Endpoint | Description | Request Body | Response | Auth Required |
|--------|----------|-------------|--------------|----------|---------------|
| POST | `/users/` | Register user (old) | `UserCreate` | `UserRead` (201) | No |
| POST | `/users/register` | Register user (old) | `UserCreate` | `UserRead` (201) | No |
| POST | `/users/login` | Authenticate user (old) | `UserLogin` | `UserRead` (200) | No |
| GET | `/users/{user_id}` | Get user details | - | `UserRead` (200) | No |

### Calculation Endpoints (BREAD) - Module 14 Authenticated

| Method | Endpoint | Description | Request Body | Response | BREAD Operation |
|--------|----------|-------------|--------------|----------|-----------------|
| POST | `/api/calculations/` | **Add** new calculation | `CalculationCreate` | `CalculationRead` (201) | Add |
| GET | `/api/calculations/` | **Browse** all user calculations | - | `List[CalculationRead]` (200) | Browse |
| GET | `/api/calculations/{calc_id}` | **Read** specific calculation | - | `CalculationRead` (200) | Read |
| PUT | `/api/calculations/{calc_id}` | **Edit** existing calculation | `CalculationUpdate` | `CalculationRead` (200) | Edit |
| DELETE | `/api/calculations/{calc_id}` | **Delete** calculation | - | None (204) | Delete |

**Note**: All `/api/calculations/*` endpoints require a valid JWT token in the `Authorization: Bearer <token>` header. Users can only access their own calculations.

### Legacy Calculation Endpoints (No Authentication - For Backward Compatibility)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/calculations/` | Create calculation | No |
| GET | `/calculations/` | Get all calculations | No |
| GET | `/calculations/{calc_id}` | Get specific calculation | No |
| PUT | `/calculations/{calc_id}` | Update calculation | No |
| DELETE | `/calculations/{calc_id}` | Delete calculation | No |

## Data Models

### User Model
```python
id: int (primary key)
username: str (unique, 3-50 chars)
email: str (unique, valid email format)
password_hash: str (PBKDF2-SHA256 hashed)
created_at: datetime (server default)
bio: str (optional, max 500 chars) [NEW - Final Project]
profile_updated_at: datetime (optional) [NEW - Final Project]
calculations: List[Calculation] (relationship, cascade delete)
```

### Calculation Model
```python
id: int (primary key)
a: float (first operand)
b: float (second operand)
type: str (Add, Sub, Multiply, or Divide)
user_id: int (optional, foreign key to User)
user: User (relationship back to User)
result: float (computed on-the-fly in schema)
```

## Schemas

### User Schemas
- **UserCreate**: `{username, email, password}` - For registration
- **UserRead**: `{id, username, email, created_at}` - Response model
- **UserLogin**: `{username, password}` - For login

### Calculation Schemas
- **CalculationCreate**: `{a, b, type}` - For creating calculations
- **CalculationRead**: `{id, a, b, type, user_id, result}` - Response model with computed result
- **CalculationUpdate**: `{a?, b?, type?}` - For partial updates (all fields optional)
- **CalcType**: Enum with values `Add`, `Sub`, `Multiply`, `Divide`

## Getting Started

### Prerequisites
- Python 3.11+
- pip package manager
- Docker (optional)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Tejen1710/Final-Project.git
   cd Final-Project
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Option 1: Direct with Uvicorn**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Option 2: Using Docker**
```bash
docker build -t fastapi-calculator .
docker run -p 8000:8000 fastapi-calculator
```

**Option 3: Using Docker Compose**
```bash
docker-compose up
```

Once running, access the API documentation at: **http://127.0.0.1:8000/docs**

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run with verbose output:**
```bash
pytest -v
```

**Run only unit tests:**
```bash
pytest tests/unit/ -v
```

**Run only integration tests:**
```bash
pytest tests/integration/ -v
```

**Run E2E tests (requires running server):**
```bash
pytest tests/e2e/ -v
```

**Run specific test file:**
```bash
pytest tests/integration/test_users_calculations_api.py -v
```

**Run Final Project profile tests:**
```bash
# Unit tests
pytest tests/unit/test_password_change.py -v

# Integration tests
pytest tests/integration/test_profile_api.py -v

# E2E tests
pytest tests/e2e/test_profile_e2e.py -v
```

**Run with coverage report:**
```bash
pytest --cov=app
```

### Database Configuration

**For SQLite (default, development):**
```bash
# Automatically uses ./test.db or ./test_db.db
pytest
```

**For PostgreSQL (testing):**
```bash
# PowerShell
$env:DATABASE_URL = "postgresql://user:password@localhost:5432/calculator_test"
pytest

# Linux/macOS
export DATABASE_URL="postgresql://user:password@localhost:5432/calculator_test"
pytest
```

## Usage Examples

### 1. Register a New User (Get JWT Token)
```bash
curl -X POST "http://127.0.0.1:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Login (Get JWT Token)
```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Add a Calculation (Requires JWT)
```bash
curl -X POST "http://127.0.0.1:8000/api/calculations/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "a": 15,
    "b": 3,
    "type": "Multiply"
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "a": 15.0,
  "b": 3.0,
  "type": "Multiply",
  "user_id": 1,
  "result": 45.0
}
```

### 4. Browse All Calculations (Requires JWT)
```bash
curl -X GET "http://127.0.0.1:8000/api/calculations/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response (200):**
```json
[
  {
    "id": 1,
    "a": 15.0,
    "b": 3.0,
    "type": "Multiply",
    "user_id": 1,
    "result": 45.0
  },
  {
    "id": 2,
    "a": 10.0,
    "b": 5.0,
    "type": "Add",
    "user_id": 1,
    "result": 15.0
  }
]
```

### 5. Read Specific Calculation (Requires JWT)
```bash
curl -X GET "http://127.0.0.1:8000/api/calculations/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 6. Edit/Update a Calculation (Requires JWT)
```bash
curl -X PUT "http://127.0.0.1:8000/api/calculations/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"type": "Divide"}'
```

**Response (200):**
```json
{
  "id": 1,
  "a": 15.0,
  "b": 3.0,
  "type": "Divide",
  "user_id": 1,
  "result": 5.0
}
```

### 7. Delete a Calculation (Requires JWT)
```bash
curl -X DELETE "http://127.0.0.1:8000/api/calculations/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response (204 No Content)**

### 8. Get User Profile (Requires JWT) - Final Project Feature
```bash
curl -X GET "http://127.0.0.1:8000/profile" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Response (200):**
```json
{
  "id": 1,
  "username": "john123",
  "email": "john@example.com",
  "bio": "Calculator enthusiast",
  "created_at": "2024-01-15T10:30:00",
  "profile_updated_at": "2024-01-20T14:45:00"
}
```

### 9. Update User Profile (Requires JWT) - Final Project Feature
```bash
curl -X PUT "http://127.0.0.1:8000/profile" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "email": "newemail@example.com",
    "bio": "Updated bio information"
  }'
```

**Response (200):**
```json
{
  "id": 1,
  "username": "john123",
  "email": "newemail@example.com",
  "bio": "Updated bio information",
  "created_at": "2024-01-15T10:30:00",
  "profile_updated_at": "2024-01-21T09:15:00"
}
```

### 10. Change Password (Requires JWT) - Final Project Feature
```bash
curl -X POST "http://127.0.0.1:8000/change-password" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "current_password": "oldpassword123",
    "new_password": "newpassword456",
    "confirm_password": "newpassword456"
  }'
```

**Response (200):**
```json
{
  "message": "Password changed successfully"
}
```

## Frontend Usage

### Access the Web Interface
1. **Start the server** (see Running the Application above)
2. **Register**: Navigate to `http://127.0.0.1:8000/static/register.html`
3. **Login**: Navigate to `http://127.0.0.1:8000/static/login.html`
4. **Manage Calculations**: After login, you'll be redirected to `http://127.0.0.1:8000/static/calculations.html`
5. **User Profile**: Access your profile at `http://127.0.0.1:8000/static/profile.html` 🆕

### Calculations Manager Features
- **Browse**: View all your calculations in a list with results
- **Add**: Create new calculations with operation type selection
- **Edit**: Update existing calculations (click Edit button on any calculation)
- **Delete**: Remove calculations with confirmation dialog
- **Client-Side Validation**: Checks for divide-by-zero, valid numbers, required fields
- **Automatic Redirects**: Session expiry detection redirects to login page

### User Profile Features 🆕 Final Project
- **View Profile**: See your username, email, and account creation date
- **Update Profile**: Change your email address or add/edit your bio
- **Change Password**: Securely update your password with current password verification
- **Navigation**: Quick links to calculations page and logout
- **Validation**: Client-side and server-side validation for all inputs
- **Auto-Logout**: After password change, you're logged out and must re-login

## Test Coverage

### Test Summary
- **Total Tests**: 90+ ✅
- **Unit Tests**: 39 (factory, schemas, security, password/profile validation)
- **Integration Tests**: 40+ (user + calculation + profile API)
- **E2E Tests**: 21+ (authentication + BREAD operations + profile workflows)

### E2E Test Coverage (Module 14 + Final Project)

**Calculations BREAD E2E Tests:**
- ✅ Add calculation with valid data (positive)
- ✅ Add calculation - divide by zero validation (negative)
- ✅ Browse all calculations (positive)
- ✅ Browse empty calculations list (positive)
- ✅ Edit calculation successfully (positive)
- ✅ Edit non-existent calculation (negative)
- ✅ Delete calculation successfully (positive)
- ✅ Add calculation with missing fields (negative)
- ✅ Unauthorized access without token (negative)
- ✅ Multiple operation types (Add, Sub, Multiply, Divide)

**Authentication E2E Tests:**
- ✅ Register with valid data (positive)
- ✅ Login with valid credentials (positive)
- ✅ Register with invalid email (negative)
- ✅ Register with short password (negative)
- ✅ Login with wrong password (negative)

**Profile Management E2E Tests (Final Project):** 🆕
- ✅ View profile workflow (login → view → verify data displayed)
- ✅ Update profile workflow (login → update bio → verify persistence)
- ✅ Change password workflow (login → change → logout → re-login)
- ✅ Wrong current password error handling (negative)
- ✅ Password mismatch validation (negative)
- ✅ Profile navigation (profile ↔ calculations)
- ✅ Logout from profile page
- ✅ Unauthorized profile access redirect (negative)

### Key Test Categories

**User Authentication Tests:**
- JWT token generation and validation
- Successful registration and login
- Duplicate email validation
- Email format validation
- Password strength validation
- Login with correct/incorrect credentials
- Session expiry handling

**Calculation BREAD Tests (Authenticated):**
- Create calculations (all operation types: Add, Sub, Multiply, Divide)
- Divide-by-zero validation (client & server)
- Browse user-specific calculations
- Read specific calculation by ID
- Edit calculations with partial updates
- Delete calculations with confirmation
- User data isolation (users can only see their own data)

**Integration Tests:**
- Full workflow (register → login → create calculations)
- Multiple users with isolated calculation data
- JWT authentication on all calculation endpoints
- Database persistence
- Relationship integrity (user-calculation)

## BREAD Operations Details

### ADD (CREATE)
- **Endpoint**: `POST /calculations/`
- **Authentication**: Required (JWT Bearer token)
- **Validation**: Numeric operands, valid operation type, divide-by-zero check
- **Response**: 201 Created with full resource including computed result
- **User Scoping**: Calculation automatically associated with authenticated user

### BROWSE (READ ALL)
- **Endpoint**: `GET /calculations/`
- **Authentication**: Required (JWT Bearer token)
- **Response**: 200 OK with array of user's calculations
- **User Scoping**: Returns only calculations belonging to authenticated user

### READ (READ ONE)
- **Endpoint**: `GET /calculations/{calc_id}`
- **Authentication**: Required (JWT Bearer token)
- **Response**: 200 OK with calculation details
- **Error**: 404 Not Found if doesn't exist or doesn't belong to user

### EDIT (UPDATE)
- **Endpoint**: `PUT /calculations/{calc_id}`
- **Authentication**: Required (JWT Bearer token)
- **Features**: Partial updates, field-level flexibility
- **Response**: 200 OK with updated resource
- **Error**: 404 Not Found if doesn't exist or doesn't belong to user

### DELETE
- **Endpoint**: `DELETE /calculations/{calc_id}`
- **Authentication**: Required (JWT Bearer token)
- **Response**: 204 No Content
- **Error**: 404 Not Found if doesn't exist or doesn't belong to user

## Security Features
- **JWT Authentication**: Bearer token required for all calculation and profile operations
- **User Data Isolation**: Users can only access their own calculations and profile
- **Password Hashing**: PBKDF2-SHA256 algorithm (secure, no salt issues)
- **Token Expiration**: 60-minute expiry on JWT tokens
- **Password Change Verification**: Current password must be verified before changing 🆕
- **Password Validation**: Minimum 8 characters, match confirmation required 🆕
- **Input Validation**: Pydantic schemas with type hints for all requests
- **Email Validation**: Ensures unique email addresses across users 🆕
- **Error Handling**: Appropriate HTTP status codes (401, 404, 400, etc.)
- **Database Constraints**: Unique constraints on username and email
- **Relationships**: CASCADE delete for data integrity
- **Dependency Injection**: FastAPI's dependency system for database sessions
- **HTTPBearer Security**: Standardized security scheme for token handling

## Docker Deployment

### Build Image
```bash
docker build -t fastapi-calculator:latest .
```

### Run Container
```bash
docker run -d \
  -p 8000:8000 \
  --name calculator-app \
  fastapi-calculator:latest
```

### Using Docker Compose
```bash
docker-compose up -d
```

### Check Logs
```bash
docker logs calculator-app
```

### Stop Container
```bash
docker stop calculator-app
```

## Environment Variables
- `DATABASE_URL`: Database connection string (default: `sqlite:///./test.db`)
- `PORT`: Server port (default: `8000`)
- `HOST`: Server host (default: `0.0.0.0`)

## Complete BREAD Operations with Authentication

### Key Features

**Authenticated Calculation Endpoints:**
- All calculation BREAD operations require JWT authentication
- Users can only access their own calculation data
- Complete user data isolation and security

**Comprehensive Frontend:**
- Full-featured calculations manager (`calculations.html`)
- Tabbed interface for Browse, Add, and Edit operations
- Real-time validation and error handling
- Automatic session expiry detection and redirect
- Delete functionality with confirmation dialogs

**Enhanced E2E Testing:**
- Complete BREAD operation test coverage
- Positive and negative test scenarios
- Authentication flow testing
- User data isolation verification

### Playwright E2E Tests

**Install Playwright browsers:**
```bash
python -m playwright install chromium
```

**Run E2E tests:**
```bash
# Run all E2E tests
pytest tests/e2e/ -v

# Run specific E2E test files
pytest tests/e2e/test_register_e2e.py -v
pytest tests/e2e/test_login_e2e.py -v
pytest tests/e2e/test_calculations_e2e.py -v

# Run with headed browser (see the tests run)
pytest tests/e2e/ -v --headed

# Run E2E tests with server already running
uvicorn app.main:app --reload
pytest tests/e2e/ -v
```

**E2E Test Files:**
- `test_register_e2e.py` - User registration tests
- `test_login_e2e.py` - User login tests
- `test_calculations_e2e.py` - **NEW** Complete BREAD operations tests

### CI/CD Pipeline

**GitHub Actions Workflow:**
1. Checkout code
2. Set up Python 3.11
3. Install dependencies from requirements.txt
4. Install Playwright browsers
5. Run unit and integration tests
6. Start FastAPI server in background
7. Run Playwright E2E tests (including new BREAD tests)
8. Login to Docker Hub (if tests pass)
9. Build and push Docker image to Docker Hub (if tests pass)

**View workflow:** `.github/workflows/ci.yml`

**Docker Hub Repository:** `tejenthakkar1710/final-project-calculator`

**Docker Hub Link:** https://hub.docker.com/r/tejenthakkar1710/final-project-calculator

**Secrets Required:**
- `DOCKERHUB_USERNAME` - Your Docker Hub username
- `DOCKERHUB_TOKEN` - Your Docker Hub access token

### Testing Workflow

**Complete test suite:**
```bash
# 1. Run unit and integration tests
pytest tests/unit tests/integration tests/test_*.py -v

# 2. Start server for E2E tests
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
sleep 5

# 3. Run E2E tests
pytest tests/e2e/ -v

# 4. Run all tests together
pytest -v
```

**Test individual components:**
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# E2E tests only (BREAD operations)
pytest tests/e2e/test_calculations_e2e.py -v
```

## Final Project Submission Checklist

### Required Implementation ✅
- [x] **New Feature**: User Profile & Password Management
- [x] **Backend**: 3 new authenticated API endpoints (GET/PUT profile, POST change-password)
- [x] **Database**: User model updated with `bio` and `profile_updated_at` fields
- [x] **Schemas**: UserProfile, UserProfileUpdate, PasswordChange with validation
- [x] **CRUD Operations**: update_user_profile(), change_user_password()
- [x] **Frontend**: New `profile.html` page with forms and client-side validation
- [x] **Frontend Logic**: `profile.js` with API integration and error handling
- [x] **Unit Tests**: Password hashing, schema validation (10+ tests)
- [x] **Integration Tests**: Profile API endpoints with DB verification (12+ tests)
- [x] **E2E Tests**: Complete workflow tests with Playwright (8+ tests)
- [x] **Documentation**: Updated README with feature documentation

### Test Coverage for Final Project Feature 📊
- **Unit Tests** (test_password_change.py): 10+ tests
  - Password hashing and verification
  - PasswordChange schema validation
  - UserProfileUpdate schema validation
- **Integration Tests** (test_profile_api.py): 12+ tests
  - Get profile (authenticated/unauthenticated)
  - Update profile (success/email conflict/partial updates)
  - Change password (success/wrong current/mismatch/too short)
- **E2E Tests** (test_profile_e2e.py): 8+ tests
  - Full workflow: login → view → update → verify
  - Password change workflow: change → logout → re-login
  - Validation and error handling
  - Navigation and security

### Module 14 Checklist ✅
- [x] Complete BREAD endpoints with JWT authentication
- [x] Frontend `calculations.html` with all operations
- [x] Comprehensive E2E tests for BREAD operations
- [x] Updated GitHub Actions CI/CD workflow
- [x] Updated README with complete documentation
- [x] reflection.md with project insights

### Screenshots to Provide 📸
1. **GitHub Actions Workflow** - Successful CI/CD run with all tests passing
2. **Docker Hub** - Pushed image in repository
3. **Frontend BREAD Operations**:
   - Browse calculations page
   - Add calculation form
   - Edit calculation form
   - Delete confirmation dialog
4. **Profile Feature** 🆕:
   - Profile page showing user info
   - Profile update form
   - Password change form
   - Success/error messages

### Links to Provide 🔗
- GitHub Repository URL
- Docker Hub Repository URL

### Learning Outcomes Demonstrated ✅
- **CLO3**: Automated testing with pytest (90+ tests)
- **CLO4**: GitHub Actions CI/CD with Docker deployment
- **CLO9**: Docker containerization (Dockerfile + docker-compose)
- **CLO10**: REST API creation and testing (FastAPI endpoints)
- **CLO11**: SQL database integration (SQLAlchemy ORM)
- **CLO12**: JSON validation with Pydantic schemas
- **CLO13**: Secure authentication (JWT, password hashing, verification)

## Dependencies

Key packages:
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **sqlalchemy**: ORM
- **pydantic**: Data validation
- **passlib**: Password hashing with PBKDF2-SHA256
- **python-jose**: JWT token generation and validation
- **pytest**: Testing framework
- **httpx**: HTTP client for testing
- **playwright**: Browser automation for E2E tests

See `requirements.txt` for complete list.

## Backward Compatibility

This module maintains backward compatibility with Module 11:
- Old `/users/` endpoint still works (calls same `create_user` function as `/users/register`)
- All existing tests pass
- Database schema unchanged
- CRUD operation signatures compatible

## Validation Rules

### User Registration
- **Username**: 3-50 characters, unique
- **Email**: Valid email format, unique
- **Password**: Minimum 8 characters

### User Profile Update 🆕
- **Email**: Valid email format, must be unique (can't use another user's email)
- **Bio**: Optional, max 500 characters

### Password Change 🆕
- **Current Password**: Required, must match existing password
- **New Password**: Minimum 8 characters
- **Confirm Password**: Must match new password

### Calculation Creation
- **a, b**: Float values (positive or negative)
- **type**: Must be one of: `Add`, `Sub`, `Multiply`, `Divide`
- **Division**: `b` cannot be zero when type is `Divide`

## Error Handling

Common HTTP Status Codes:
- `200 OK`: Successful GET/PUT/POST
- `201 Created`: Successful resource creation
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation error (duplicate username/email)
- `401 Unauthorized`: Invalid login credentials
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Invalid request data format

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

**Tejen Thakkar**
- GitHub: [@Tejen1710](https://github.com/Tejen1710)
- Repository: [Module-14](https://github.com/Tejen1710/Module-14)

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PBKDF2 Password Hashing](https://passlib.readthedocs.io/)