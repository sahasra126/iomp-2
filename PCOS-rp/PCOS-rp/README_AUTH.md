# PCOS Predictor with PostgreSQL Authentication

This application provides PCOS risk assessment using machine learning with user authentication powered by PostgreSQL.

## Features

- ✅ User Registration and Login with PostgreSQL
- ✅ JWT Token-based Authentication
- ✅ Protected PCOS Prediction Routes
- ✅ Prediction History Storage
- ✅ Secure Password Hashing

## Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

## Backend Setup

### 1. Install PostgreSQL

Download and install PostgreSQL from https://www.postgresql.org/download/

### 2. Create Database

Open PostgreSQL command line (psql) or pgAdmin and run:

```sql
CREATE DATABASE pcos_db;
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend` folder:

```env
SECRET_KEY=your-secret-key-change-this-to-something-secure
DB_HOST=localhost
DB_NAME=pcos_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_PORT=5432
```

**Important:** Change `DB_PASSWORD` to your PostgreSQL password!

### 4. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Train the Model (if not already done)

```bash
python train_model.py
```

This will create the required model files:
- `pcos_model.pkl`
- `pcos_scaler.pkl`
- `feature_names.pkl`

### 6. Run the Backend Server

```bash
python app_with_auth.py
```

The backend will:
- Automatically create database tables (users and predictions)
- Start on http://localhost:5000

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start the React App

```bash
npm start
```

The frontend will start on http://localhost:3000

## Usage

### 1. Register a New Account

- Navigate to http://localhost:3000
- Click "Register" in the navbar
- Fill in your details:
  - Full Name
  - Email
  - Password (minimum 6 characters)
- Click "Register"

### 2. Login

- Click "Login" in the navbar
- Enter your email and password
- Click "Login"

### 3. Make PCOS Predictions

- Once logged in, go to "Predict PCOS"
- Fill in the medical parameters
- Click "Predict PCOS Risk"
- Your prediction will be saved to your account history

### 4. Logout

- Click "Logout" in the navbar to end your session

## Database Tables

### users table
```sql
- id: Serial Primary Key
- email: VARCHAR(255) UNIQUE
- password_hash: VARCHAR(255)
- full_name: VARCHAR(255)
- created_at: TIMESTAMP
- last_login: TIMESTAMP
```

### predictions table
```sql
- id: Serial Primary Key
- user_id: INTEGER (Foreign Key to users)
- prediction_result: INTEGER
- probability: FLOAT
- risk_level: VARCHAR(50)
- input_data: JSONB
- created_at: TIMESTAMP
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user (requires auth)

### Predictions
- `POST /predict` - Make PCOS prediction (requires auth)
- `GET /predictions/history` - Get user's prediction history (requires auth)

### Public
- `GET /` - API info
- `GET /health` - Health check
- `GET /features` - Get feature info

## Security Features

- ✅ Password hashing using Werkzeug
- ✅ JWT token-based authentication
- ✅ Protected routes requiring authentication
- ✅ Secure password storage (never stored in plain text)
- ✅ CORS protection
- ✅ SQL injection prevention using parameterized queries

## Troubleshooting

### Backend Issues

**Database Connection Error:**
```
Check your .env file and ensure:
- PostgreSQL is running
- Database 'pcos_db' exists
- Credentials are correct
```

**Model Not Found:**
```bash
python train_model.py
```

### Frontend Issues

**Cannot Connect to Server:**
- Make sure backend is running on http://localhost:5000
- Check CORS settings in app_with_auth.py

**Authentication Not Working:**
- Clear browser localStorage
- Check that JWT token is being sent in requests
- Verify SECRET_KEY matches in .env

## Testing

### Test Registration
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'
```

### Test Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### Test Prediction (with token)
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"Age":28,"BMI":24,"Insulin":10,"Testosterone":40,"LH":7,"FSH":6,"Glucose":90,"Cholesterol":180}'
```

## Tech Stack

### Backend
- Flask (Web Framework)
- PostgreSQL (Database)
- psycopg2 (PostgreSQL adapter)
- PyJWT (JWT tokens)
- Werkzeug (Password hashing)
- scikit-learn (ML model)

### Frontend
- React (UI Framework)
- React Router (Routing)
- Axios (HTTP client)
- Context API (State management)

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.
