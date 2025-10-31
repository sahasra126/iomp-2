# 📋 PCOS Predictor - Setup Checklist

Use this checklist to ensure everything is set up correctly!

## ✅ Pre-Installation Checklist

- [ ] Python 3.8 or higher installed
  - Check: `python --version`
  
- [ ] Node.js 16 or higher installed
  - Check: `node --version`
  
- [ ] PostgreSQL 12 or higher installed
  - Check: `psql --version`
  
- [ ] Git installed (optional)
  - Check: `git --version`

---

## ✅ Database Setup Checklist

- [ ] PostgreSQL service is running
  - Windows: Check Services, look for "postgresql"
  - Mac/Linux: `sudo service postgresql status`

- [ ] **Run the automated database setup script** ⭐ **RECOMMENDED**
  - **File:** `database_setup.sql` (in project root)
  - **Option 1 - Command Line:** `psql -U postgres -f database_setup.sql`
  - **Option 2 - pgAdmin:** Open pgAdmin → Query Tool → Open `database_setup.sql` → Execute
  - **What it does:** Creates `pcos_db` database + all 6 tables automatically
  - **For detailed help:** See `DATABASE_SETUP_INSTRUCTIONS.md`

- [ ] Verify database setup was successful
  - Test: `psql -U postgres -d pcos_db -c "\dt"`
  - Should show 6 tables: users, user_profiles, symptom_logs, lifestyle_predictions, predictions, cycle_info
  - Should see success message: "✅ Database tables created successfully!"

**Alternative (Manual Setup):**
- [ ] Created database `pcos_db` manually
  - Command: `psql -U postgres -c "CREATE DATABASE pcos_db;"`
  - Then tables will auto-create when backend starts

---

## ✅ Backend Setup Checklist

- [ ] Navigated to `backend` folder
  - `cd backend`

- [ ] Created Python virtual environment
  - Windows: `python -m venv venv`
  - Mac/Linux: `python3 -m venv venv`

- [ ] Activated virtual environment
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`
  - You should see `(venv)` in your terminal prompt

- [ ] Installed Python dependencies
  - `pip install -r requirements.txt`
  - Should install: Flask, PostgreSQL driver, ML libraries, etc.

- [ ] Created `.env` file from template
  - Copy `.env.example` to `.env`
  - Or manually create `.env` file

- [ ] Updated `.env` with your database credentials
  - [ ] DB_HOST (usually `localhost`)
  - [ ] DB_NAME (should be `pcos_db`)
  - [ ] DB_USER (your PostgreSQL username)
  - [ ] DB_PASSWORD (your PostgreSQL password)
  - [ ] SECRET_KEY (change to random string!)

- [ ] ML model files present
  - [ ] `pcos_model.pkl` exists
  - [ ] `pcos_scaler.pkl` exists
  - [ ] `feature_names.pkl` exists
  - [ ] `lifestyle_pcos_model.pkl` exists
  - [ ] `lifestyle_scaler.pkl` exists
  - [ ] `lifestyle_features.pkl` exists

- [ ] Backend starts successfully
  - Run: `python app.py`
  - Should see: "Running on http://127.0.0.1:5000"
  - Should see: "✅ Database tables initialized successfully"
  - Should see: "✅ Clinical model loaded successfully"
  - Should see: "✅ Lifestyle model loaded successfully"

---

## ✅ Frontend Setup Checklist

- [ ] Navigated to `frontend` folder
  - `cd frontend` (from project root)

- [ ] Installed Node.js dependencies
  - `npm install`
  - This may take 2-5 minutes
  - Should create `node_modules` folder

- [ ] Verified `src/config.js` exists
  - Contains API_BASE_URL configuration

- [ ] Updated API URL if needed
  - Default uses local IP for network access
  - Change to `http://localhost:5000` if only using on same machine
  - Change to backend server IP if backend is on different machine

- [ ] Frontend starts successfully
  - Run: `npm start`
  - Should automatically open browser to http://localhost:3000
  - No compilation errors in terminal

---

## ✅ Testing Checklist

### Basic Functionality
- [ ] Frontend loads without errors
- [ ] Can see Login and Register buttons
- [ ] Navbar displays correctly

### Registration & Login
- [ ] Can register a new user
  - Fill in: Name, Email, Password, Age
  - Click "Register"
  - Should redirect to login or home page

- [ ] Can login with registered user
  - Enter email and password
  - Click "Login"
  - Should see user name in top-right corner

### Lifestyle Assessment
- [ ] Click "Lifestyle Assessment" in navbar
- [ ] Step 1: Basic Info loads
  - Can enter Age, Height, Weight, Cycle info
  - "Next" button works

- [ ] Step 2: Symptoms loads
  - Can select symptom checkboxes
  - Can go "Back" to Step 1
  - "Next" button works

- [ ] Step 3: Lifestyle loads
  - Can select family history, stress, exercise, sleep
  - "Submit Assessment" button works

- [ ] Results display
  - Shows risk level (Low/Moderate/High)
  - Shows risk score percentage
  - Shows top risk factors
  - Shows recommendations

### Symptom Tracker
- [ ] Click "Symptom Tracker" in navbar
- [ ] Can select a date on calendar
- [ ] Can select period flow intensity
- [ ] Can check symptom boxes
- [ ] "Save Today's Entry" button works
- [ ] Shows success message after saving

### Assessment History
- [ ] Click user name in top-right
- [ ] Dropdown menu appears
- [ ] Click "Assessment History"
- [ ] Shows list of past assessments
- [ ] Can expand assessment cards
- [ ] Shows questions, answers, risk factors, recommendations

### Clinical Prediction (if you have lab values)
- [ ] Click "Clinical Prediction" in navbar
- [ ] Can enter lab values
- [ ] Submit works
- [ ] Shows prediction result

---

## ✅ Network Access Checklist (Optional)

If you want to access from other devices on the same network:

- [ ] Found your computer's IP address
  - Windows: `ipconfig` → IPv4 Address
  - Mac: `ifconfig | grep inet`
  - Linux: `hostname -I`

- [ ] Backend running with `host='0.0.0.0'`
  - Check `app.py` line: `app.run(debug=True, host='0.0.0.0')`

- [ ] Updated CORS in backend
  - Check `app.py` includes your IP in origins list

- [ ] Updated `frontend/src/config.js`
  - API_BASE_URL uses IP address instead of localhost

- [ ] Firewall allows connections
  - Windows: Allow Python and Node through Windows Firewall
  - Mac/Linux: Check firewall settings for ports 3000 and 5000

- [ ] Can access from other device
  - From phone/tablet/laptop on same WiFi
  - Visit: `http://YOUR_IP:3000`
  - Should load the app

---

## 🔧 Troubleshooting

### ❌ Database connection error
**Fix:** Check PostgreSQL is running, verify credentials in `.env`

### ❌ Port already in use
**Fix:** Close other apps using port 3000/5000, or change port in code

### ❌ ML model not found
**Fix:** Ensure all `.pkl` files are in `backend/` folder

### ❌ Module not found errors
**Fix:** Activate virtual environment, run `pip install -r requirements.txt`

### ❌ npm install fails
**Fix:** Delete `node_modules` and `package-lock.json`, run `npm install` again

### ❌ CORS error from other device
**Fix:** Add device IP to CORS origins in `backend/app.py`

---

## 📞 Quick Commands Reference

### Start Backend:
```bash
cd backend
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
python app.py
```

### Start Frontend:
```bash
cd frontend
npm start
```

### Access Application:
- Local: http://localhost:3000
- Network: http://YOUR_IP:3000

---

## ✨ All Done!

If all checkboxes are checked, your PCOS Predictor is ready to use! 🎉

If you have issues, refer to README.md for detailed instructions.
