-- Lifestyle Prediction Database Schema

-- User health profiles (one-time comprehensive data)
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    height FLOAT,  -- in cm
    weight FLOAT,  -- in kg
    bmi FLOAT,
    waist_circumference FLOAT,  -- in cm
    family_history_pcos BOOLEAN DEFAULT FALSE,
    family_history_diabetes BOOLEAN DEFAULT FALSE,
    family_history_obesity BOOLEAN DEFAULT FALSE,
    ethnicity VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Menstrual cycle information
CREATE TABLE IF NOT EXISTS cycle_info (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    cycle_regularity VARCHAR(20),  -- Regular, Irregular, VeryIrregular
    average_cycle_length INTEGER,  -- days
    last_period_date DATE,
    periods_missed_3months INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Daily symptom logs
CREATE TABLE IF NOT EXISTS symptom_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    log_date DATE NOT NULL,
    
    -- Physical symptoms (0-10 scale or boolean)
    acne_severity INTEGER DEFAULT 0,  -- 0: None, 1-3: Mild, 4-6: Moderate, 7-10: Severe
    hirsutism_score INTEGER DEFAULT 0,  -- Facial/body hair growth
    hair_loss_score INTEGER DEFAULT 0,  -- Scalp hair thinning
    skin_darkening BOOLEAN DEFAULT FALSE,  -- Acanthosis nigricans
    skin_tags BOOLEAN DEFAULT FALSE,
    
    -- Metabolic symptoms
    fatigue_level INTEGER DEFAULT 0,  -- 0-10
    weight_change FLOAT DEFAULT 0,  -- kg change from previous log
    
    -- Mental/emotional
    mood_swings INTEGER DEFAULT 0,  -- 0-10
    anxiety_level INTEGER DEFAULT 0,  -- 0-10
    depression_score INTEGER DEFAULT 0,  -- 0-10
    
    -- Other symptoms
    sleep_quality INTEGER DEFAULT 5,  -- 0-10
    food_cravings INTEGER DEFAULT 0,  -- 0-10
    bloating INTEGER DEFAULT 0,  -- 0-10
    headache BOOLEAN DEFAULT FALSE,
    
    -- Period tracking
    period_flow VARCHAR(20),  -- None, Light, Medium, Heavy
    period_active BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lifestyle data logs
CREATE TABLE IF NOT EXISTS lifestyle_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    log_date DATE NOT NULL,
    
    -- Exercise
    exercise_minutes INTEGER DEFAULT 0,
    exercise_type VARCHAR(100),  -- Cardio, Strength, Yoga, etc.
    
    -- Diet
    diet_quality INTEGER DEFAULT 5,  -- 0-10 self-assessment
    sugar_intake INTEGER DEFAULT 5,  -- 0-10 (0=none, 10=very high)
    processed_food INTEGER DEFAULT 5,  -- 0-10
    water_intake INTEGER DEFAULT 0,  -- glasses per day
    
    -- Stress & Sleep
    stress_level INTEGER DEFAULT 5,  -- 0-10
    sleep_hours FLOAT DEFAULT 7.0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lifestyle-based PCOS risk predictions
CREATE TABLE IF NOT EXISTS lifestyle_predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    
    -- Prediction results
    risk_score FLOAT NOT NULL,  -- 0.0 to 1.0
    risk_level VARCHAR(20) NOT NULL,  -- Low, Moderate, High
    confidence FLOAT,  -- Model confidence
    
    -- Risk factors breakdown (JSON)
    risk_factors JSONB,  -- {"cycle_irregularity": 0.8, "bmi": 0.6, ...}
    
    -- Recommendations
    recommendations JSONB,  -- Personalized suggestions
    
    -- Model info
    model_version VARCHAR(20),
    prediction_type VARCHAR(50) DEFAULT 'lifestyle',  -- lifestyle or clinical
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_symptom_logs_user_date ON symptom_logs(user_id, log_date);
CREATE INDEX idx_lifestyle_logs_user_date ON lifestyle_logs(user_id, log_date);
CREATE INDEX idx_lifestyle_predictions_user ON lifestyle_predictions(user_id, created_at DESC);
CREATE INDEX idx_cycle_info_user ON cycle_info(user_id);

-- Add trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cycle_info_updated_at BEFORE UPDATE ON cycle_info
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
