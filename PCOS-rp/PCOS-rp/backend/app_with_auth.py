from flask import Flask, request, jsonify, session
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
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
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
    print(f"✅ Model loaded successfully with features: {feature_names}")
except FileNotFoundError as e:
    print(f"❌ Error loading model files: {e}")
    print("Please run train_model.py first to train the model.")
    model, scaler, feature_names = None, None, None

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

@app.route("/predictions/history", methods=["GET"])
@token_required
def get_prediction_history(current_user_id):
    """Get user's prediction history"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """SELECT id, prediction_result, probability, risk_level, 
                      input_data, created_at 
               FROM predictions 
               WHERE user_id = %s 
               ORDER BY created_at DESC 
               LIMIT 20""",
            (current_user_id,)
        )
        predictions = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'predictions': [dict(p) for p in predictions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get history: {str(e)}'}), 500

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

if __name__ == "__main__":
    # Initialize database on startup
    init_db()
    app.run(debug=True, port=5000)
