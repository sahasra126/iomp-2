# app_with_auth.py
from flask import Flask, request, jsonify, make_response, Response
from flask_cors import CORS
import joblib
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
import jwt
from functools import wraps

# ---------------- APP ----------------
app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-me')
app.config['PROPAGATE_EXCEPTIONS'] = True

# ---------------- CORS ----------------
ALLOWED_ORIGINS = {
    "https://iomp-2.vercel.app",
    "https://iomp-2-knlko6wgi-sahas-projects-905bce4f.vercel.app",
    "https://iomp-2-git-main-sahas-projects-905bce4f.vercel.app"
}

# --- FIX: Ensure preflight OPTIONS is handled before auth decorators run ---
@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        # Return an empty response so browser preflight succeeds.
        return make_response('', 200)

# Keep lightweight custom CORS so we control credentials and vary header
@app.after_request
def add_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin and origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response

# (Optional) keep explicit OPTIONS catch-all routes — not required because of before_request,
# but harmless and sometimes useful for health checks from load balancers.
@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path=''):
    return make_response('', 200)

# ---------------- DATABASE CONFIG ----------------
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'pcos_db'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
    'port': os.environ.get('DB_PORT', '5432')
}

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    try:
        from urllib.parse import urlparse, unquote
        url = urlparse(DATABASE_URL)
        DB_CONFIG = {
            'host': url.hostname,
            'database': url.path.lstrip('/'),
            'user': unquote(url.username) if url.username else None,
            'password': unquote(url.password) if url.password else None,
            'port': str(url.port) if url.port else '5432'
        }
        print("Using DATABASE_URL from env for DB connection")
    except Exception as e:
        print("Failed to parse DATABASE_URL:", e)

# ---------------- MODEL LOADING ----------------
model = scaler = None
feature_names = []

try:
    model = joblib.load("pcos_model.pkl")
    scaler = joblib.load("pcos_scaler.pkl")
    feature_names = joblib.load("feature_names.pkl")
    try:
        feature_names = feature_names.tolist()
    except Exception:
        feature_names = list(feature_names)
    print("✅ Model loaded with features:", feature_names)
except Exception as e:
    print("❌ Failed to load model or features on startup:", e)
    model, scaler, feature_names = None, None, []

# ---------------- DB HELPERS ----------------
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("❌ Database connection error:", e)
        return None

def init_db():
    conn = get_db_connection()
    if not conn:
        print("init_db: no DB connection available")
        return
    cur = None
    try:
        cur = conn.cursor()
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
        print("✅ Database ready (tables ensured)")
    except Exception as e:
        print("❌ DB Init Error:", e)
        try:
            conn.rollback()
        except:
            pass
    finally:
        try:
            if cur:
                cur.close()
            if conn:
                conn.close()
        except:
            pass

# safe to call at import/startup
try:
    init_db()
except Exception as e:
    print("Warning: init_db failed on import:", e)

# ---------------- AUTH DECORATOR ----------------
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Allow preflight requests to pass through without token
        if request.method == 'OPTIONS':
            return make_response('', 200)

        header = request.headers.get("Authorization", "")
        if not header:
            return jsonify({"error": "Token missing"}), 401

        token = header
        if header.startswith("Bearer "):
            token = header.split(" ", 1)[1]

        try:
            decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            user_id = decoded.get("user_id")
            if not user_id:
                return jsonify({"error": "Invalid token payload"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            print("Token decode error:", e)
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(user_id, *args, **kwargs)
    return wrapper

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "PCOS Prediction API is running 🎉",
        "features": feature_names,
        "status": "ready" if model else "model_not_loaded"
    })

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.json or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")
    full_name = data.get("full_name", "")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database not connected"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "Email already registered"}), 409

        password_hash = generate_password_hash(password)
        cur.execute(
            "INSERT INTO users (email, password_hash, full_name) VALUES (%s, %s, %s) RETURNING id",
            (email, password_hash, full_name)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        print("Register error:", e)
        try:
            conn.rollback()
        except:
            pass
        return jsonify({"error": "Registration failed"}), 500
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass

    token = jwt.encode(
        {"user_id": user_id, "exp": datetime.utcnow() + timedelta(days=7)},
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return jsonify({"message": "Registration successful", "token": token}), 201

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database not connected"}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        print("Login DB error:", e)
        return jsonify({"error": "Login failed"}), 500

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = jwt.encode(
        {"user_id": user["id"], "exp": datetime.utcnow() + timedelta(days=7)},
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return jsonify({"message": "Login successful", "token": token}), 200

@app.route("/predict", methods=["POST"])
@token_required
def predict(user_id):
    if model is None or scaler is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.json or {}
    try:
        values = [data[f] for f in feature_names]
    except KeyError as e:
        missing = str(e)
        return jsonify({"error": f"Missing feature: {missing}"}), 400

    X = np.array([values])
    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)[0]
    probs = model.predict_proba(X_scaled)[0]
    p_pcos = float(probs[1])

    if p_pcos < 0.3:
        risk = "Low"
    elif p_pcos < 0.7:
        risk = "Moderate"
    else:
        risk = "High"

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO predictions (user_id, prediction_result, probability, risk_level, input_data)
                   VALUES (%s, %s, %s, %s, %s)""",
                (user_id, int(pred), float(p_pcos), risk, Json(data))
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error saving prediction: {e}")

    return jsonify({
        "pcos_risk": int(pred),
        "probability": round(p_pcos, 3),
        "risk_level": risk,
        "input": data
    })

@app.route("/predictions/history", methods=["GET"])
@token_required
def history(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM predictions WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print("History DB error:", e)
        return jsonify({'error': 'Failed to fetch history'}), 500

    return jsonify({"history": rows})

@app.route("/features", methods=["GET"])
def get_features():
    return jsonify({"features": feature_names})

@app.route("/health", methods=["GET"])
def health():
    db_conn = get_db_connection()
    db_connected = db_conn is not None
    if db_conn:
        try:
            db_conn.close()
        except:
            pass
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "feature_count": len(feature_names),
        "database_connected": db_connected
    })

# ---------------- START (local dev) ----------------
if __name__ == "__main__":
    init_db()
    app.run(port=5000, debug=True)
