from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
import jwt
from functools import wraps

app = Flask(__name__)
# Allow CORS from localhost and network IP
CORS(app, supports_credentials=True, origins=[
    "http://localhost:3000",
    "http://192.168.0.104:3000",
    "http://172.20.10.3:3000",
    "http://127.0.0.1:3000"
])
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'pcos_db'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
    'port': os.environ.get('DB_PORT', '5432')
}

# Load model, scaler, and feature names
try:
    model = joblib.load("pcos_model.pkl")
    scaler = joblib.load("pcos_scaler.pkl")
    feature_names = joblib.load("feature_names.pkl")
    print(f"✅ Clinical model loaded successfully with features: {feature_names}")
except FileNotFoundError as e:
    print(f"❌ Error loading clinical model files: {e}")
    print("Please run train_model.py first to train the model.")
    model, scaler, feature_names = None, None, None

# Load lifestyle prediction model
try:
    lifestyle_model = joblib.load("lifestyle_pcos_model.pkl")
    lifestyle_scaler = joblib.load("lifestyle_scaler.pkl")
    lifestyle_features = joblib.load("lifestyle_features.pkl")
    print(f"✅ Lifestyle model loaded successfully with features: {lifestyle_features}")
except FileNotFoundError as e:
    print(f"❌ Error loading lifestyle model files: {e}")
    print("Please run train_lifestyle_model.py first.")
    lifestyle_model, lifestyle_scaler, lifestyle_features = None, None, None

def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    if not conn:
        print("❌ Could not connect to database")
        return False
    
    try:
        cur = conn.cursor()
        
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        
        # Create predictions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                prediction_result INTEGER NOT NULL,
                probability FLOAT NOT NULL,
                risk_level VARCHAR(50),
                input_data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create user_profiles table
        cur.execute("""
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
            )
        """)
        
        # Create symptom_logs table
        cur.execute("""
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
            )
        """)
        
        # Create lifestyle_predictions table
        cur.execute("""
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
            )
        """)
        
        conn.commit()
        print("✅ Database tables initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def token_required(f):
    """Decorator to require JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "PCOS Prediction API with Authentication",
        "features": feature_names.tolist() if feature_names is not None else [],
        "status": "ready" if model is not None else "model not loaded"
    })

@app.route("/auth/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')
        age = data.get('age', None)  # Optional age field
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor()
        
        # Check if user already exists
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'Email already registered'}), 409
        
        # Hash password and create user
        password_hash = generate_password_hash(password)

        # Build a username fallback: prefer explicit username, else full_name prefix, else email prefix
        username = data.get('username') if data.get('username') else None
        if not username:
            if full_name:
                username = ''.join(full_name.split()).lower()
            else:
                username = email.split('@')[0]

        # Check whether the users table has a username column. If so, include it; otherwise insert without it.
        try:
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='username'")
            has_username_col = cur.fetchone() is not None
        except Exception:
            has_username_col = False

        # Check for age column
        try:
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='age'")
            has_age_col = cur.fetchone() is not None
        except Exception:
            has_age_col = False

        # Build INSERT query based on available columns
        if has_username_col and has_age_col:
            cur.execute(
                "INSERT INTO users (email, password_hash, full_name, username, age) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (email, password_hash, full_name, username, age)
            )
        elif has_username_col:
            cur.execute(
                "INSERT INTO users (email, password_hash, full_name, username) VALUES (%s, %s, %s, %s) RETURNING id",
                (email, password_hash, full_name, username)
            )
        else:
            cur.execute(
                "INSERT INTO users (email, password_hash, full_name) VALUES (%s, %s, %s) RETURNING id",
                (email, password_hash, full_name)
            )
        user_id = cur.fetchone()[0]
        conn.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'full_name': full_name
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@app.route("/auth/login", methods=["POST"])
def login():
    """Login user"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get user from database
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        
        if not user or not check_password_hash(user['password_hash'], password):
            cur.close()
            conn.close()
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Update last login if column exists
        try:
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='last_login'")
            if cur.fetchone():
                cur.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s", (user['id'],))
                conn.commit()
        except Exception:
            pass  # Column doesn't exist, skip updating last_login
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'full_name': user['full_name']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@app.route("/auth/me", methods=["GET"])
@token_required
def get_current_user(current_user_id):
    """Get current user info"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, email, full_name, username, age, created_at, updated_at FROM users WHERE id = %s", (current_user_id,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': dict(user)}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get user: {str(e)}'}), 500

@app.route("/predict", methods=["POST"])
@token_required
def predict(current_user_id):
    """Make PCOS prediction (requires authentication)"""
    if model is None or scaler is None:
        return jsonify({
            "error": "Model not loaded. Please train the model first."
        }), 500
    
    try:
        data = request.json
        
        # Validate input data
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract features in the correct order
        try:
            features_array = np.array([[data[feature] for feature in feature_names]])
        except KeyError as e:
            missing_feature = str(e).strip("'")
            return jsonify({
                "error": f"Missing required feature: {missing_feature}",
                "required_features": feature_names.tolist()
            }), 400
        
        # Scale the features
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Calculate risk level
        pcos_probability = probabilities[1]
        if pcos_probability < 0.3:
            risk_level = "Low"
        elif pcos_probability < 0.7:
            risk_level = "Moderate"
        else:
            risk_level = "High"
        
        # Save prediction to database
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    """INSERT INTO predictions 
                       (user_id, prediction_result, probability, risk_level, input_data) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (current_user_id, int(prediction), float(pcos_probability), risk_level, 
                     psycopg2.extras.Json(data))
                )
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Error saving prediction: {e}")
        
        return jsonify({
            "pcos_risk": int(prediction),
            "probability": round(pcos_probability, 3),
            "healthy_probability": round(probabilities[0], 3),
            "risk_level": risk_level,
            "prediction_text": "PCOS Likely" if prediction == 1 else "Healthy",
            "confidence": round(max(probabilities), 3),
            "input_features": data
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        }), 500

@app.route("/features", methods=["GET"])
def get_features():
    """Get the list of required features for prediction"""
    if feature_names is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    feature_info = {
        "Age": {"description": "Age in years", "typical_range": "18-45"},
        "BMI": {"description": "Body Mass Index", "typical_range": "18-35"},
        "Insulin": {"description": "Insulin level (μIU/mL)", "typical_range": "5-25"},
        "Testosterone": {"description": "Testosterone level (ng/dL)", "typical_range": "15-85"},
        "LH": {"description": "Luteinizing Hormone (mIU/mL)", "typical_range": "2-20"},
        "FSH": {"description": "Follicle Stimulating Hormone (mIU/mL)", "typical_range": "3-12"},
        "Glucose": {"description": "Glucose level (mg/dL)", "typical_range": "70-140"},
        "Cholesterol": {"description": "Cholesterol level (mg/dL)", "typical_range": "150-250"}
    }
    
    return jsonify({
        "features": feature_names.tolist(),
        "feature_info": feature_info
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    conn = get_db_connection()
    db_connected = conn is not None
    if conn:
        conn.close()
    
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "features_count": len(feature_names) if feature_names is not None else 0,
        "database_connected": db_connected
    })

@app.route("/predictions/history", methods=["GET"])
@token_required
def get_prediction_history(current_user_id):
    """Get user's prediction history"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check if predictions table has any columns by querying information_schema
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'predictions' AND table_schema = 'public'
        """)
        columns = [row['column_name'] for row in cur.fetchall()]
        
        # Only select columns that exist
        if 'prediction_result' in columns:
            cur.execute(
                """SELECT id, prediction_result, probability, risk_level, 
                          input_data, created_at 
                   FROM predictions 
                   WHERE user_id = %s 
                   ORDER BY created_at DESC 
                   LIMIT 20""",
                (current_user_id,)
            )
        else:
            # If predictions table doesn't have the expected structure, return empty
            return jsonify({'predictions': []}), 200
        
        predictions = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'predictions': [dict(p) for p in predictions]
        }), 200
        
    except Exception as e:
        print(f"Error getting prediction history: {str(e)}")
        # Return empty array instead of error to not break the frontend
        return jsonify({'predictions': []}), 200

# ============================================================================
# LIFESTYLE ASSESSMENT ENDPOINTS
# ============================================================================

@app.route("/lifestyle/assess", methods=["POST"])
@token_required
def lifestyle_assessment(current_user_id):
    """Perform lifestyle-based PCOS risk assessment"""
    if lifestyle_model is None or lifestyle_scaler is None:
        return jsonify({
            "error": "Lifestyle model not loaded. Please train the model first."
        }), 500
    
    try:
        data = request.json
        
        # Extract and validate lifestyle features
        required_fields = lifestyle_features
        
        # Build feature array
        feature_values = []
        for feature in lifestyle_features:
            if feature not in data:
                return jsonify({
                    "error": f"Missing required field: {feature}",
                    "required_fields": lifestyle_features
                }), 400
            feature_values.append(float(data[feature]))
        
        # Scale features and predict
        features_array = np.array([feature_values])
        features_scaled = lifestyle_scaler.transform(features_array)
        
        prediction = lifestyle_model.predict(features_scaled)[0]
        probabilities = lifestyle_model.predict_proba(features_scaled)[0]
        
        pcos_probability = probabilities[1]
        
        # Determine risk level
        if pcos_probability < 0.3:
            risk_level = "Low"
        elif pcos_probability < 0.7:
            risk_level = "Moderate"
        else:
            risk_level = "High"
        
        # Generate risk factors breakdown
        risk_factors = {}
        feature_importance = lifestyle_model.feature_importances_
        for i, feature in enumerate(lifestyle_features):
            risk_factors[feature] = {
                "value": float(data[feature]),
                "importance": float(feature_importance[i])
            }
        
        # Generate recommendations based on risk factors
        recommendations = generate_recommendations(data, risk_level)
        
        # Save to database
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                
                # Save user profile if provided
                if 'height' in data and 'weight' in data:
                    bmi = float(data['weight']) / ((float(data['height'])/100) ** 2)
                    cur.execute("""
                        INSERT INTO user_profiles 
                        (user_id, height, weight, bmi, family_history_pcos, family_history_diabetes)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE SET
                            height = EXCLUDED.height,
                            weight = EXCLUDED.weight,
                            bmi = EXCLUDED.bmi,
                            updated_at = CURRENT_TIMESTAMP
                    """, (current_user_id, float(data['height']), float(data['weight']), 
                          bmi, data.get('FamilyHistory', 0) == 1, False))
                
                # Save lifestyle prediction
                cur.execute("""
                    INSERT INTO lifestyle_predictions 
                    (user_id, risk_score, risk_level, confidence, risk_factors, 
                     recommendations, model_version, prediction_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (current_user_id, float(pcos_probability), risk_level,
                      float(max(probabilities)), psycopg2.extras.Json(risk_factors),
                      psycopg2.extras.Json(recommendations), '1.0', 'lifestyle'))
                
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Error saving lifestyle prediction: {e}")
        
        return jsonify({
            "pcos_risk": int(prediction),
            "probability": round(pcos_probability, 3),
            "healthy_probability": round(probabilities[0], 3),
            "risk_level": risk_level,
            "prediction_text": "PCOS Risk Detected" if prediction == 1 else "Low Risk",
            "confidence": round(max(probabilities), 3),
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "input_features": data
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Lifestyle assessment failed: {str(e)}"
        }), 500


def generate_recommendations(data, risk_level):
    """Generate personalized recommendations based on assessment"""
    recommendations = []
    
    # BMI recommendations
    bmi = data.get('BMI', 0)
    if bmi > 25:
        recommendations.append({
            "category": "Weight Management",
            "priority": "high",
            "title": "Focus on Weight Management",
            "description": "Your BMI indicates you may benefit from weight management. Even a 5-10% weight loss can significantly improve PCOS symptoms.",
            "actions": ["Consult a nutritionist", "Start with 150 minutes of exercise per week", "Track your food intake"]
        })
    
    # Cycle irregularity
    cycle_reg = data.get('CycleRegularity', 0)
    if cycle_reg >= 1:
        recommendations.append({
            "category": "Menstrual Health",
            "priority": "high",
            "title": "Track Your Menstrual Cycle",
            "description": "Irregular cycles are a key PCOS symptom. Regular tracking helps identify patterns.",
            "actions": ["Use our symptom tracker daily", "Note cycle length and flow", "Consult a gynecologist if cycles are consistently irregular"]
        })
    
    # Exercise
    exercise_freq = data.get('ExerciseFrequency', 0)
    if exercise_freq < 3:
        recommendations.append({
            "category": "Physical Activity",
            "priority": "medium",
            "title": "Increase Physical Activity",
            "description": "Regular exercise helps manage PCOS symptoms, improve insulin sensitivity, and reduce stress.",
            "actions": ["Aim for 30 minutes of activity 5 days a week", "Try a mix of cardio and strength training", "Start with walking or yoga"]
        })
    
    # Stress management
    stress_level = data.get('StressLevel', 0)
    if stress_level > 6:
        recommendations.append({
            "category": "Mental Health",
            "priority": "high",
            "title": "Manage Stress Levels",
            "description": "High stress can worsen PCOS symptoms by affecting hormones.",
            "actions": ["Practice meditation or mindfulness", "Ensure 7-8 hours of sleep", "Consider counseling or therapy", "Try stress-reduction techniques like yoga"]
        })
    
    # Sleep quality
    sleep_quality = data.get('SleepQuality', 10)
    if sleep_quality < 5:
        recommendations.append({
            "category": "Sleep Hygiene",
            "priority": "medium",
            "title": "Improve Sleep Quality",
            "description": "Poor sleep affects hormone balance and can worsen PCOS symptoms.",
            "actions": ["Maintain a regular sleep schedule", "Avoid screens before bedtime", "Create a relaxing bedtime routine"]
        })
    
    # Hirsutism
    hirsutism = data.get('Hirsutism', 0)
    if hirsutism > 1:
        recommendations.append({
            "category": "Symptom Management",
            "priority": "medium",
            "title": "Address Excess Hair Growth",
            "description": "Excess hair growth is a common PCOS symptom related to elevated androgens.",
            "actions": ["Consult a dermatologist", "Consider treatments like laser hair removal", "Check hormone levels with your doctor"]
        })
    
    # General recommendation based on risk level
    if risk_level == "High":
        recommendations.insert(0, {
            "category": "Medical Consultation",
            "priority": "urgent",
            "title": "Consult a Healthcare Provider",
            "description": "Your assessment suggests a higher risk of PCOS. Please consult a gynecologist or endocrinologist for proper diagnosis and treatment.",
            "actions": ["Schedule an appointment with a gynecologist", "Get blood tests (hormones, glucose, insulin)", "Discuss ultrasound examination if needed"]
        })
    
    return recommendations


@app.route("/lifestyle/save-symptom-log", methods=["POST"])
@token_required
def save_symptom_log(current_user_id):
    """Save daily symptom log"""
    try:
        data = request.json
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO symptom_logs 
            (user_id, log_date, acne_severity, hirsutism_score, hair_loss_score,
             fatigue_level, mood_swings, anxiety_level, sleep_quality, 
             food_cravings, bloating, period_flow, period_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            current_user_id,
            data.get('date', datetime.now().date()),
            data.get('acne', 0),
            data.get('hirsutism', 0),
            data.get('hairLoss', 0),
            data.get('fatigue', 0),
            data.get('moodChanges', 0),
            data.get('anxiety', 0),
            data.get('sleepQuality', 5),
            data.get('foodCravings', 0),
            data.get('bloating', 0),
            data.get('periodFlow', 'None'),
            data.get('periodActive', False)
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'message': 'Symptom log saved successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': f'Failed to save symptom log: {str(e)}'}), 500


@app.route("/lifestyle/prediction-history", methods=["GET"])
@token_required
def get_lifestyle_prediction_history(current_user_id):
    """Get user's lifestyle prediction history"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT id, risk_score, risk_level, confidence, 
                   risk_factors, recommendations, created_at
            FROM lifestyle_predictions
            WHERE user_id = %s AND prediction_type = 'lifestyle'
            ORDER BY created_at DESC
            LIMIT 20
        """, (current_user_id,))
        
        predictions = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify({
            'predictions': [dict(p) for p in predictions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get history: {str(e)}'}), 500


if __name__ == "__main__":
    # Initialize database on startup
    init_db()
    # host='0.0.0.0' allows connections from other devices on the network
    app.run(debug=True, host='0.0.0.0', port=5000)
