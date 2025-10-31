# PCOS Predictor - Complete Setup Guide

A comprehensive PCOS (Polycystic Ovary Syndrome) prediction and tracking application with lifestyle-based and clinical assessments.

## 🎯 Features

- **Lifestyle Assessment**: Get PCOS risk assessment without blood tests (97.75% accuracy)
- **Clinical Prediction**: Lab-value based prediction for users with test results
- **Symptom Tracker**: Daily symptom and cycle tracking
- **Assessment History**: View all past predictions with detailed recommendations
- **User Authentication**: Secure JWT-based login and registration

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **Node.js 16+** - [Download](https://nodejs.org/)
3. **PostgreSQL 12+** - [Download](https://www.postgresql.org/download/)
4. **Git** (optional) - [Download](https://git-scm.com/)

---

## 🚀 Installation & Setup

### Step 1: Extract the Project

Extract the ZIP file to your desired location:
```
PCOS-rp/
├── backend/
├── frontend/
├── dataset/
└── README.md
```

---

### Step 2: Database Setup

#### 🎯 EASY METHOD (Recommended)

We've included a complete database setup script that creates everything automatically!

1. **Start PostgreSQL** (if not already running)
   - **Windows**: Open pgAdmin or start PostgreSQL service
   - **Mac/Linux**: `sudo service postgresql start`

2. **Run the setup script**:
   ```bash
   # Option A: Command line
   psql -U postgres -f database_setup.sql
   
   # Option B: pgAdmin
   # Open pgAdmin → Connect → Right-click on PostgreSQL → Query Tool
   # Then: File → Open → Select "database_setup.sql" → Execute (F5)
   ```

That's it! The script creates the database and all 6 tables automatically. ✅

**📖 For detailed instructions, see [`DATABASE_SETUP_INSTRUCTIONS.md`](DATABASE_SETUP_INSTRUCTIONS.md)**

---

#### 📝 Manual Method (Alternative)

If you prefer to set up manually:

**2.1 Create Database**
```sql
CREATE DATABASE pcos_db;
```

**2.2 Create Database User (Optional)**
```sql
CREATE USER pcos_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE pcos_db TO pcos_user;
```

**2.3 Initialize Database Tables**

Connect to the database and run:

```sql
-- Connect to pcos_db first
\c pcos_db

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    height FLOAT,
    weight FLOAT,
    bmi FLOAT,
    family_history_pcos BOOLEAN DEFAULT FALSE,
    family_history_diabetes BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Symptom logs
CREATE TABLE IF NOT EXISTS symptom_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    log_date DATE NOT NULL,
    acne_severity INTEGER DEFAULT 0,
    hirsutism_score INTEGER DEFAULT 0,
    hair_loss_score INTEGER DEFAULT 0,
    fatigue_level INTEGER DEFAULT 0,
    mood_swings INTEGER DEFAULT 0,
    anxiety_level INTEGER DEFAULT 0,
    sleep_quality INTEGER DEFAULT 5,
    food_cravings INTEGER DEFAULT 0,
    bloating INTEGER DEFAULT 0,
    period_flow VARCHAR(20),
    period_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lifestyle predictions
CREATE TABLE IF NOT EXISTS lifestyle_predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    risk_score FLOAT NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    confidence FLOAT,
    risk_factors JSONB,
    recommendations JSONB,
    model_version VARCHAR(20),
    prediction_type VARCHAR(50) DEFAULT 'lifestyle',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clinical predictions
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    prediction_result INTEGER NOT NULL,
    probability FLOAT NOT NULL,
    risk_level VARCHAR(50),
    input_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Step 3: Backend Setup

#### 3.1 Navigate to Backend Directory

```bash
cd backend
```

#### 3.2 Create Python Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3.3 Install Python Dependencies

```bash
pip install flask flask-cors psycopg2-binary scikit-learn joblib numpy pandas pyjwt werkzeug
```

Or if you have a requirements.txt:
```bash
pip install -r requirements.txt
```

#### 3.4 Configure Database Connection

Create a `.env` file in the `backend` folder:

```env
SECRET_KEY=your-secret-key-here-change-this-in-production
DB_HOST=localhost
DB_NAME=pcos_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
```

**⚠️ IMPORTANT**: Change these values to match your PostgreSQL setup!

#### 3.5 Start Backend Server

```bash
python app.py
```

You should see:
```
✅ Clinical model loaded successfully
✅ Lifestyle model loaded successfully
✅ Database tables initialized successfully
* Running on http://127.0.0.1:5000
* Running on http://YOUR_IP:5000
```

---

### Step 4: Frontend Setup

#### 4.1 Open New Terminal and Navigate to Frontend

```bash
cd frontend
```

#### 4.2 Install Node Dependencies

```bash
npm install
```

This will install:
- React
- React Router
- Axios
- Other dependencies from package.json

#### 4.3 Configure API URL

**If running on the same machine:**
The default configuration should work (uses your local IP).

**If backend is on a different machine:**
Edit `frontend/src/config.js`:

```javascript
// Change this to your backend server IP
const API_BASE_URL = 'http://YOUR_BACKEND_IP:5000';

export default API_BASE_URL;
```

#### 4.4 Start Frontend Development Server

```bash
npm start
```

The application will open at:
- **http://localhost:3000** (same machine)
- **http://YOUR_IP:3000** (accessible from other devices on network)

---

## 🌐 Accessing from Other Devices

### On the Same Network:

1. Find your computer's IP address:
   - **Windows**: `ipconfig` → Look for "IPv4 Address"
   - **Mac**: `ifconfig | grep inet`
   - **Linux**: `hostname -I`

2. From another device on the same network, visit:
   ```
   http://YOUR_IP:3000
   ```

3. Make sure your firewall allows connections on ports 3000 and 5000.

---

## 📱 Usage

### 1. Register/Login
- Create a new account with email, password, name, and age
- Login to access all features

### 2. Lifestyle Assessment
- No blood tests required!
- Answer questions about age, BMI, cycle, symptoms, and lifestyle
- Get instant risk assessment with personalized recommendations

### 3. Clinical Prediction (Optional)
- For users who have lab test results
- Enter values for insulin, testosterone, hormones, glucose, cholesterol
- Get clinical prediction based on lab values

### 4. Symptom Tracker
- Track daily symptoms and menstrual cycle
- Record period flow, acne, fatigue, mood changes, etc.
- Build a history of your symptoms

### 5. View History
- Click your name in the top-right corner
- Select "Assessment History"
- View all past assessments with detailed results

---

## 🔧 Troubleshooting

### Database Connection Error

**Error**: `password authentication failed for user "postgres"`

**Solution**: Update `backend/.env` with correct database credentials.

### Port Already in Use

**Error**: `Port 3000/5000 is already in use`

**Solution**: 
- Kill the process using the port
- Or change the port in the code

### CORS Error from Other Device

**Error**: Network error when accessing from different laptop

**Solution**: Make sure `backend/app.py` line 14 includes your IP:
```python
CORS(app, supports_credentials=True, origins=[
    "http://localhost:3000",
    "http://YOUR_IP:3000"
])
```

### ML Model Not Found

**Error**: `FileNotFoundError: pcos_model.pkl`

**Solution**: Make sure these files exist in `backend/`:
- `pcos_model.pkl`
- `pcos_scaler.pkl`
- `feature_names.pkl`
- `lifestyle_pcos_model.pkl`
- `lifestyle_scaler.pkl`
- `lifestyle_features.pkl`

---

## 📊 Project Structure

```
PCOS-rp/
├── backend/
│   ├── app.py                          # Main Flask server
│   ├── train_lifestyle_model.py        # ML model training
│   ├── *.pkl                           # Trained ML models
│   ├── .env                            # Database config (create this)
│   └── requirements.txt                # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/                 # React components
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── LifestyleAssessment.js
│   │   │   ├── PCOSForm.js
│   │   │   ├── SymptomTracker.js
│   │   │   ├── History.js
│   │   │   └── ...
│   │   ├── context/
│   │   │   └── AuthContext.js          # Authentication
│   │   └── config.js                   # API URL config
│   ├── package.json
│   └── public/
├── dataset/
│   └── PCOS_infertility.csv            # Training dataset
└── README.md                            # This file
```

---

## 🔐 Security Notes

**⚠️ For Production Deployment:**

1. Change `SECRET_KEY` in `.env` to a strong random string
2. Use environment variables instead of hardcoded values
3. Enable HTTPS
4. Use a production WSGI server (Gunicorn) instead of Flask dev server
5. Use a production-grade database with proper backups
6. Implement rate limiting
7. Add input validation and sanitization
8. Use strong password policies

---

## 🛠️ Technology Stack

**Backend:**
- Flask (Python web framework)
- PostgreSQL (Database)
- scikit-learn (Machine Learning)
- JWT (Authentication)

**Frontend:**
- React 18
- React Router v6
- Axios (HTTP client)
- Context API (State management)

**Machine Learning:**
- Random Forest Classifier
- 97.75% accuracy on lifestyle model
- Features: Age, BMI, Cycle info, Symptoms, Lifestyle factors

---

## 📝 Database Schema

### Tables:
- **users**: User authentication and profile
- **user_profiles**: Health profile data
- **lifestyle_predictions**: Lifestyle assessment results
- **predictions**: Clinical prediction results
- **symptom_logs**: Daily symptom tracking

---

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure database is running and configured correctly
4. Check browser console for frontend errors
5. Check terminal for backend errors

---

## 📄 License

This project is for educational and research purposes.

---

## ✨ Credits

Developed with Flask, React, and scikit-learn.

**Machine Learning Model**: Random Forest with 97.75% test accuracy
**Dataset**: PCOS infertility dataset

---

**Happy Tracking! 🌸**
