# Quick Start Guide - PCOS Predictor with Authentication

## 🚀 Fast Setup (5 minutes)

### Step 1: Install PostgreSQL

1. Download PostgreSQL: https://www.postgresql.org/download/windows/
2. Install with default settings
3. Remember your password during installation!

### Step 2: Create Database

Open **pgAdmin** or **SQL Shell (psql)** and run:

```sql
CREATE DATABASE pcos_db;
```

Or use the provided SQL file:
```bash
psql -U postgres -f backend/setup_database.sql
```

### Step 3: Backend Setup

```powershell
# Navigate to backend folder
cd backend

# Run setup script (creates venv, installs packages, trains model)
setup.bat

# Edit .env file with your PostgreSQL password
notepad .env

# Start the backend
python app_with_auth.py
```

### Step 4: Frontend Setup

Open a **new terminal**:

```powershell
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start the frontend
npm start
```

### Step 5: Test It Out! 🎉

1. Open http://localhost:3000
2. Click **Register** to create an account
3. Fill in your details and register
4. Go to **Predict PCOS** and try it out!

---

## 📝 Manual Setup (if scripts don't work)

### Backend

```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install flask flask-cors joblib numpy scikit-learn pandas psycopg2-binary PyJWT werkzeug

# Create .env file
echo SECRET_KEY=your-secret-key-here > .env
echo DB_HOST=localhost >> .env
echo DB_NAME=pcos_db >> .env
echo DB_USER=postgres >> .env
echo DB_PASSWORD=YOUR_PASSWORD_HERE >> .env
echo DB_PORT=5432 >> .env

# Train model
python train_model.py

# Start server
python app_with_auth.py
```

### Frontend

```powershell
cd frontend

# Install dependencies
npm install

# Start app
npm start
```

---

## ✅ Verify Everything Works

### Check Backend
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "database_connected": true
}
```

### Check Frontend
Open http://localhost:3000 - you should see the PCOS Predictor homepage

---

## 🔐 Default Configuration

- **Backend:** http://localhost:5000
- **Frontend:** http://localhost:3000
- **Database:** localhost:5432
- **Database Name:** pcos_db
- **Database User:** postgres

---

## 🐛 Common Issues

### "Cannot connect to database"
- Make sure PostgreSQL is running
- Check your password in `.env` file
- Verify database `pcos_db` exists

### "Module not found"
- Activate virtual environment: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

### "Model not found"
- Run: `python train_model.py`

### "Port already in use"
- Backend (5000): Close other Flask apps or change port in `app_with_auth.py`
- Frontend (3000): Kill other React apps or change port in `package.json`

### "CORS error"
- Make sure backend is running
- Check backend URL in frontend code (should be http://localhost:5000)

---

## 📦 What Gets Created

### Backend Files
- `venv/` - Python virtual environment
- `.env` - Environment variables (contains passwords - DO NOT COMMIT!)
- `pcos_model.pkl` - Trained ML model
- `pcos_scaler.pkl` - Feature scaler
- `feature_names.pkl` - Model features

### Database Tables
- `users` - User accounts
- `predictions` - Prediction history

### Frontend
- `node_modules/` - NPM packages
- Build files in browser cache

---

## 🎯 Next Steps

1. ✅ Register an account
2. ✅ Login
3. ✅ Try sample data (Low/Moderate/High risk profiles)
4. ✅ Make a prediction
5. ✅ View your results
6. ✅ Logout and login again to verify persistence

---

## 🔒 Security Notes

- Never commit `.env` file to git
- Change `SECRET_KEY` in production
- Use strong passwords
- Keep PostgreSQL updated
- Use HTTPS in production

---

## 📞 Need Help?

- Check `README_AUTH.md` for detailed documentation
- Review error messages in terminal
- Make sure all prerequisites are installed
- Verify PostgreSQL is running

---

**Happy Predicting! 🏥**
