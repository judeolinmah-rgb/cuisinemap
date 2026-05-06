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
