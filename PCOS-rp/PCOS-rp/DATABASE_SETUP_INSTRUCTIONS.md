# 🗄️ Database Setup Instructions

## Quick Setup (Recommended)

### Step 1: Create Database
```sql
CREATE DATABASE pcos_db;
```

### Step 2: Run Setup Script
```bash
# Option A: Using psql command line
psql -U postgres -d pcos_db -f database_setup.sql

# Option B: Using psql interactive mode
psql -U postgres -d pcos_db
\i database_setup.sql

# Option C: Using pgAdmin
# 1. Open pgAdmin
# 2. Connect to your PostgreSQL server
# 3. Right-click on 'pcos_db' database → Query Tool
# 4. Open 'database_setup.sql' file
# 5. Click Execute (F5)
```

### Step 3: Verify Setup
```sql
-- Check that all tables were created
\dt

-- You should see these 6 tables:
-- ✓ users
-- ✓ user_profiles
-- ✓ symptom_logs
-- ✓ lifestyle_predictions
-- ✓ predictions
-- ✓ cycle_info
```

---

## What Gets Created

The `database_setup.sql` script automatically creates:

### 📋 Tables

1. **users** - User authentication and basic info
2. **user_profiles** - Health profile data (height, weight, BMI, family history)
3. **symptom_logs** - Daily symptom tracking (acne, fatigue, mood, etc.)
4. **lifestyle_predictions** - Lifestyle-based risk assessment results
5. **predictions** - Clinical prediction results
6. **cycle_info** - Menstrual cycle information

### 🔍 Indexes
- Performance indexes on frequently queried columns
- Foreign key relationships
- Unique constraints where needed

### 🔐 Relationships
- All user-related tables link to `users` table
- Cascade deletes (if user deleted, their data is too)

---

## Manual Setup (If Script Doesn't Work)

If the automated script has issues, you can also find individual SQL files in the `backend/` folder:

- `backend/setup_database.sql` - Basic user and prediction tables
- `backend/lifestyle_schema.sql` - Lifestyle tracking tables

---

## Troubleshooting

### Issue: "database does not exist"
**Solution:** Make sure you created the database first:
```sql
CREATE DATABASE pcos_db;
```

### Issue: "permission denied"
**Solution:** Make sure you're logged in as a user with CREATE privileges:
```bash
psql -U postgres
# Enter your postgres password
```

### Issue: "table already exists"
**Solution:** The script uses `CREATE TABLE IF NOT EXISTS` so this is safe. If you want to start fresh:
```sql
DROP DATABASE pcos_db;
CREATE DATABASE pcos_db;
-- Then run the setup script again
```

### Issue: Can't find the SQL file
**Solution:** Make sure you're in the correct directory:
```bash
# Navigate to project root
cd PCOS-rp

# Check file exists
ls database_setup.sql

# Run from correct location
psql -U postgres -d pcos_db -f database_setup.sql
```

---

## Verify Everything Works

After setup, run this query to check:

```sql
-- Connect to database
\c pcos_db

-- Check all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Should return:
-- users
-- user_profiles  
-- symptom_logs
-- lifestyle_predictions
-- predictions
-- cycle_info
```

---

## Next Steps

After database is set up:

1. ✅ Configure `backend/.env` file with database credentials
2. ✅ Start the backend server: `python app.py`
3. ✅ Start the frontend: `npm start`
4. ✅ Register a new user account
5. ✅ Start using the application!

---

## Need Help?

- See `README.md` for full setup instructions
- See `SETUP_CHECKLIST.md` for step-by-step guide
- Check `database_setup.sql` for table definitions

**Database is ready to go! 🚀**
