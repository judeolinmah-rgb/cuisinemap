const API_BASE = "http://localhost:5000/api";

// ── User ID ───────────────────────────────────────────────────────────────────
// Uses the logged-in username from ST (set by the app after login).
// Falls back to a random localStorage ID for guest/unauthenticated use.
function getUserId() {
  if (typeof ST !== "undefined" && ST && ST.username) {
    return ST.username;
  }
  const stored = localStorage.getItem("cm_username");
  if (stored) return stored;
  
  // Guest fallback
  let id = localStorage.getItem("cm_user_id");
  if (!id) {
    id = "u_" + crypto.randomUUID();
    localStorage.setItem("cm_user_id", id);
  }
  return id;
}

// ── In-memory HIST object ─────────────────────────────────────────────────────
let HIST = {
  cuisineScores: {},
  missedMeals:   {},
  hitMeals:      {},
  totalRatings:  0,
};

// ── Load history from backend ─────────────────────────────────────────────────
async function loadHistory() {
  const userId = getUserId();
  try {
    const res = await fetch(`${API_BASE}/history/${userId}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    HIST.cuisineScores = data.cuisine_scores  || {};
    HIST.missedMeals   = data.missed_meals    || {};
    HIST.hitMeals      = data.hit_meals       || {};
    HIST.totalRatings  = data.total_ratings   || 0;

    console.log("[CuisineMap] History loaded for user:", userId, {
      isNewUser: data.is_new_user,
      totalRatings: HIST.totalRatings,
    });
  } catch (err) {
    console.warn("[CuisineMap] Could not reach backend, falling back to localStorage", err);
    _loadFromLocalStorage();
  }

  if (typeof renderHistBanner        === "function") renderHistBanner();
  if (typeof renderCuisineScorePills === "function") renderCuisineScorePills();
}

// ── Save history to backend ───────────────────────────────────────────────────
async function saveHistory() {
  const userId = getUserId();
  try {
    const res = await fetch(`${API_BASE}/history/${userId}`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cuisine_scores: HIST.cuisineScores,
        missed_meals:   HIST.missedMeals,
        hit_meals:      HIST.hitMeals,
        total_ratings:  HIST.totalRatings,
      }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    console.log("[CuisineMap] History saved for user:", userId);
  } catch (err) {
    console.warn("[CuisineMap] Could not save to backend, falling back to localStorage", err);
    _saveToLocalStorage();
  }
}

// ── Reset history via backend ─────────────────────────────────────────────────
async function resetHistory() {
  const userId = getUserId();
  try {
    HIST = { cuisineScores: {}, missedMeals: {}, hitMeals: {}, totalRatings: 0 };

    const res = await fetch(`${API_BASE}/history/${userId}`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    await fetch(`${API_BASE}/history/${userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cuisine_scores: {},
        missed_meals:   {},
        hit_meals:      {},
        total_ratings:  0,
      }),
    });

    console.log("[CuisineMap] History reset for user:", userId);
  } catch (err) {
    console.warn("[CuisineMap] Could not reset on backend, clearing localStorage", err);
    localStorage.removeItem("gp_hist");
    HIST = { cuisineScores: {}, missedMeals: {}, hitMeals: {}, totalRatings: 0 };
  }

  if (typeof renderHistBanner        === "function") renderHistBanner();
  if (typeof renderCuisineScorePills === "function") renderCuisineScorePills();
}

// ── localStorage fallbacks ────────────────────────────────────────────────────
function _loadFromLocalStorage() {
  try {
    const raw = localStorage.getItem("gp_hist");
    if (raw) {
      const saved = JSON.parse(raw);
      HIST.cuisineScores = saved.cuisineScores || {};
      HIST.missedMeals   = saved.missedMeals   || {};
      HIST.hitMeals      = saved.hitMeals      || {};
      HIST.totalRatings  = saved.totalRatings  || 0;
    }
  } catch (e) {
    console.warn("[CuisineMap] localStorage fallback also failed", e);
  }
}

function _saveToLocalStorage() {
  try {
    localStorage.setItem("gp_hist", JSON.stringify(HIST));
  } catch (e) {
    console.warn("[CuisineMap] Could not save to localStorage", e);
  }
}

// ── Auto-init ─────────────────────────────────────────────────────────────────
// Note: loadHistory() is also called explicitly after login in the main app.
// This initial call handles page refreshes when the session is already active.
loadHistory();
