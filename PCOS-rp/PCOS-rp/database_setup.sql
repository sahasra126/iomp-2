-- PCOS Predictor Database Setup Script
-- Run this script to create all necessary database tables
-- 
-- Usage:
-- 1. First create the database: CREATE DATABASE pcos_db;
-- 2. Connect to it: \c pcos_db
-- 3. Run this script: \i database_setup.sql
-- Or: psql -U postgres -d pcos_db -f database_setup.sql

-- ============================================
-- Users Table
-- ============================================
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

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- ============================================
-- User Profiles Table
-- ============================================
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

CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);

-- ============================================
-- Symptom Logs Table
-- ============================================
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
    weight_gain_difficulty INTEGER DEFAULT 0,
    period_flow VARCHAR(20),
    period_active BOOLEAN DEFAULT FALSE,
    cycle_length INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_symptom_logs_user_date ON symptom_logs(user_id, log_date);
CREATE INDEX IF NOT EXISTS idx_symptom_logs_date ON symptom_logs(log_date);

-- ============================================
-- Lifestyle Predictions Table
-- ============================================
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

CREATE INDEX IF NOT EXISTS idx_lifestyle_predictions_user_id ON lifestyle_predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_lifestyle_predictions_created_at ON lifestyle_predictions(created_at);

-- ============================================
-- Clinical Predictions Table
-- ============================================
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    prediction_result INTEGER NOT NULL,
    probability FLOAT NOT NULL,
    risk_level VARCHAR(50),
    input_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at);

-- ============================================
-- Cycle Information Table
-- ============================================
CREATE TABLE IF NOT EXISTS cycle_info (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    cycle_regularity VARCHAR(20),
    average_cycle_length INTEGER,
    last_period_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

CREATE INDEX IF NOT EXISTS idx_cycle_info_user_id ON cycle_info(user_id);

-- ============================================
-- Print Success Message
-- ============================================
\echo '✅ Database tables created successfully!'
\echo ''
\echo 'Tables created:'
\echo '  - users (authentication and profile)'
\echo '  - user_profiles (health profile data)'
\echo '  - symptom_logs (daily symptom tracking)'
\echo '  - lifestyle_predictions (lifestyle assessment results)'
\echo '  - predictions (clinical prediction results)'
\echo '  - cycle_info (menstrual cycle information)'
\echo ''
\echo 'You can now start the backend server!'
