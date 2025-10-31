-- PCOS Predictor Database Setup Script
-- Run this in PostgreSQL (psql or pgAdmin)

-- Create database
CREATE DATABASE pcos_db;

-- Connect to the database
\c pcos_db

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Create predictions table
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    prediction_result INTEGER NOT NULL,
    probability FLOAT NOT NULL,
    risk_level VARCHAR(50),
    input_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_predictions_user_id ON predictions(user_id);
CREATE INDEX idx_predictions_created_at ON predictions(created_at DESC);

-- Display tables
\dt

-- Display table structures
\d users
\d predictions

SELECT 'Database setup completed successfully!' AS message;
