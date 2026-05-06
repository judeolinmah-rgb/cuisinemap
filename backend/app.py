"""
CuisineMap — Taste History API
Flask + SQLite backend for persisting user cuisine scores and feedback.
"""

from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

def utcnow():
    return datetime.now(timezone.utc).isoformat()

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app, supports_credentials=True)

DB_PATH = os.path.join(os.path.dirname(__file__), "cuisinemap.db")


# ── Database helpers ───────────────────────────────────────────────────────────

def get_db():
    """Open a database connection with row factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    with get_db() as conn:
        conn.executescript("""                           
            CREATE TABLE IF NOT EXISTS cuisines (
            cuisine_id   TEXT PRIMARY KEY,
            name         TEXT UNIQUE NOT NULL,
            region       TEXT,
            description  TEXT,
            source       TEXT
        );

            CREATE TABLE IF NOT EXISTS meals (
            meal_id      TEXT PRIMARY KEY,
            cuisine_id   TEXT NOT NULL,
            name         TEXT NOT NULL,
            description  TEXT,
            ingredients  TEXT,
            image_url    TEXT,
            source       TEXT,          
            FOREIGN KEY (cuisine_id) REFERENCES cuisines(cuisine_id)
        );              
            CREATE TABLE IF NOT EXISTS users (
                user_id       TEXT PRIMARY KEY,
                username      TEXT UNIQUE NOT NULL,
                email         TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at    TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS taste_history (
                user_id         TEXT PRIMARY KEY,
                cuisine_scores  TEXT NOT NULL DEFAULT '{}',
                missed_meals    TEXT NOT NULL DEFAULT '{}',
                total_ratings   INTEGER NOT NULL DEFAULT 0,
                updated_at      TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            CREATE TABLE IF NOT EXISTS ratings (
            user_id         TEXT NOT NULL,
            meal_id         INTEGER NOT NULL,
            rating          INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            created_at      TEXT NOT NULL,
            PRIMARY KEY (user_id, meal_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
            );               
        """)
    print(f"[CuisineMap] Database ready at {DB_PATH}")


# ── Serve frontend ────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "cuisinemap_update.html")

@app.route("/history-api.js")
def serve_js():
    return send_from_directory(BASE_DIR, "history-api.js")

@app.route("/rate")
def rate():
    return send_from_directory(BASE_DIR, "rate.html")


# ── Routes ─────────────────────────────────────────────────────────────────────

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    """Simple health check."""
    return jsonify({"status": "ok", "service": "CuisineMap API"})


@app.route("/api/register", methods=["POST"])
def register():
    """
    Register a new user account.
    Expected JSON body:
    {
        "username": "jude",
        "email": "jude@example.com",
        "password": "securepassword"
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    username = data.get("username", "").strip()
    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "Username, email and password are all required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    user_id       = secrets.token_hex(16)
    password_hash = generate_password_hash(password)
    now           = utcnow()

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO users (user_id, username, email, password_hash, created_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, username, email, password_hash, now)
            )
            conn.execute(
                "INSERT INTO taste_history (user_id, cuisine_scores, missed_meals, total_ratings, updated_at) VALUES (?, '{}', '{}', 0, ?)",
                (user_id, now)
            )
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 409

    session["user_id"]  = user_id
    session["username"] = username

    return jsonify({
        "success":  True,
        "user_id":  user_id,
        "username": username,
        "message":  "Account created successfully"
    }), 201


@app.route("/api/login", methods=["POST"])
def login():
    """
    Log in with username and password.
    Expected JSON body:
    {
        "username": "jude",
        "password": "securepassword"
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    with get_db() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    session["user_id"]  = user["user_id"]
    session["username"] = user["username"]

    return jsonify({
        "success":  True,
        "user_id":  user["user_id"],
        "username": user["username"],
        "message":  "Logged in successfully"
    })


@app.route("/api/logout", methods=["POST"])
def logout():
    """Log out the current user."""
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"})


@app.route("/api/me")
def me():
    user_id = session.get("user_id")
    username = session.get("username")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify({"user_id": user_id, "username": username})

    
@app.route("/api/history/<user_id>", methods=["GET"])
def get_history(user_id):
    """
    Load taste history for a user.
    Returns empty defaults if the user is new.
    """
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM taste_history WHERE user_id = ?", (user_id,)
        ).fetchone()
 
    if row is None:
        return jsonify({
            "user_id": user_id,
            "cuisine_scores": {},
            "missed_meals": {},
            "hit_meals": {},
            "total_ratings": 0,
            "is_new_user": True
        })
 
    # hit_meals column may not exist in older DBs — handle gracefully
    try:
        hit_meals = json.loads(row["hit_meals"])
    except (KeyError, TypeError):
        hit_meals = {}
 
    return jsonify({
        "user_id": user_id,
        "cuisine_scores": json.loads(row["cuisine_scores"]),
        "missed_meals": json.loads(row["missed_meals"]),
        "hit_meals": hit_meals,
        "total_ratings": row["total_ratings"],
        "updated_at": row["updated_at"],
        "is_new_user": False
    })


@app.route("/api/history/<user_id>", methods=["POST"])
def save_history(user_id):
    """
    Save (upsert) taste history for a user.
    Expected JSON body:
    {
        "cuisine_scores": { "italian": 2, "japanese": -1, ... },
        "missed_meals":   { "Spaghetti carbonara": true, ... },
        "hit_meals":      { "Pad Thai": 2, "Jerk chicken": 1, ... },
        "total_ratings":  12
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
 
    cuisine_scores = data.get("cuisine_scores", {})
    missed_meals   = data.get("missed_meals", {})
    hit_meals      = data.get("hit_meals", {})
    total_ratings  = data.get("total_ratings", 0)
 
    if not isinstance(cuisine_scores, dict):
        return jsonify({"error": "cuisine_scores must be an object"}), 400
    if not isinstance(missed_meals, dict):
        return jsonify({"error": "missed_meals must be an object"}), 400
    if not isinstance(hit_meals, dict):
        return jsonify({"error": "hit_meals must be an object"}), 400
    if not isinstance(total_ratings, int) or total_ratings < 0:
        return jsonify({"error": "total_ratings must be a non-negative integer"}), 400
 
    now = utcnow()
 
    with get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users (user_id, created_at) VALUES (?, ?)",
            (user_id, now)
        )
 
        conn.execute("""
            INSERT INTO taste_history (user_id, cuisine_scores, missed_meals, hit_meals, total_ratings, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                cuisine_scores = excluded.cuisine_scores,
                missed_meals   = excluded.missed_meals,
                hit_meals      = excluded.hit_meals,
                total_ratings  = excluded.total_ratings,
                updated_at     = excluded.updated_at
        """, (
            user_id,
            json.dumps(cuisine_scores),
            json.dumps(missed_meals),
            json.dumps(hit_meals),
            total_ratings,
            now
        ))
 
    return jsonify({
        "success": True,
        "user_id": user_id,
        "total_ratings": total_ratings,
        "updated_at": now
    })


@app.route("/api/history/<user_id>", methods=["DELETE"])
def reset_history(user_id):
    """
    Reset a user's taste history back to clean defaults.
    Does NOT delete the user record — just zeroes out the scores.
    """
    now = utcnow()
 
    with get_db() as conn:
        existing = conn.execute(
            "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
 
        if existing is None:
            return jsonify({"error": "User not found"}), 404
 
        conn.execute("""
            UPDATE taste_history
            SET cuisine_scores = '{}',
                missed_meals   = '{}',
                hit_meals      = '{}',
                total_ratings  = 0,
                updated_at     = ?
            WHERE user_id = ?
        """, (now, user_id))
 
    return jsonify({"success": True, "user_id": user_id})
        
@app.route("/api/cuisines", methods=["GET"])
def get_cuisines():
    """Return all cuisines with their meals."""
    with get_db() as conn:
        cuisines = conn.execute(
            "SELECT * FROM cuisines ORDER BY region, name"
        ).fetchall()
        
        result = []
        for cuisine in cuisines:
            meals = conn.execute(
                "SELECT * FROM meals WHERE cuisine_id = ?", (cuisine["cuisine_id"],)
            ).fetchall()
            
            result.append({
                "cuisine_id":  cuisine["cuisine_id"],
                "name":        cuisine["name"],
                "region":      cuisine["region"],
                "description": cuisine["description"],
                "source":      cuisine["source"],
                "meals": [
                    {
                        "meal_id":     m["meal_id"],
                        "name":        m["name"],
                        "description": m["description"],
                        "ingredients": json.loads(m["ingredients"]),
                        "image_url":   m["image_url"]
                    }
                    for m in meals
                ]
            })
    
    return jsonify({"cuisines": result, "total": len(result)})
# — Ratings —————————————————————————————————————————

@app.route("/api/dishes")
def get_dishes():
    with get_db() as conn:
        rows = conn.execute("""
            SELECT m.meal_id, m.name, m.description, m.image_url, c.name as cuisine_name
            FROM meals m
            JOIN cuisines c ON m.cuisine_id = c.cuisine_id
            ORDER BY c.name, m.name
        """).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/ratings", methods=["GET", "POST"])
def handle_ratings():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    if request.method == "GET":
        with get_db() as conn:
            rows = conn.execute(
                "SELECT meal_id, rating FROM ratings WHERE user_id = ?", (user_id,)
            ).fetchall()
        return jsonify([dict(r) for r in rows])

    if request.method == "POST":
        data = request.get_json()
        meal_id = data.get("meal_id")
        rating = data.get("rating")
        if not meal_id or not rating:
            return jsonify({"error": "Missing meal_id or rating"}), 400
        created_at = datetime.utcnow().isoformat()
        with get_db() as conn:
            conn.execute("""
                INSERT INTO ratings (user_id, meal_id, rating, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id, meal_id) DO UPDATE SET rating = excluded.rating
            """, (user_id, meal_id, rating, created_at))
        return jsonify({"success": True})
# ── Run ────────────────────────────────────────────────────────────────────────

init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
