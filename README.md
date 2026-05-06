# CuisineMap

**Personalized weekly meal planning powered by international cuisine.**

CuisineMap generates 7-day meal plans tailored to your taste history, dietary preferences, budget, and household size — drawing from cuisines across 20+ countries.

---

## Features

- **Personalized meal plans** — Generated based on your ratings, cuisine preferences, and dietary needs
- **Taste history tracking** — The app learns your preferences over time and improves recommendations
- **International cuisine library** — 20+ cuisines including Italian, Japanese, Moroccan, Lebanese, Filipino, and more
- **Multi-user support** — Each user has their own taste profile stored in the database
- **Live database** — Meal data pulled from TheMealDB API

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Meal Data | TheMealDB API |

---

## Project Background

CuisineMap began as **GlobalPlate** — a meal planner focused on global cuisine discovery. After finding the name was already taken, the project was rebranded to CuisineMap, with a sharper focus on personalization and taste-driven recommendations.

---

## Getting Started

### Prerequisites
- Python 3.x
- pip

### Installation

```bash
git clone https://github.com/judeolinmah-rgb/cuisinemap.git
cd cuisinemap/backend
pip install -r requirements.txt
python app.py
```

Then open your browser and go to `http://localhost:5000`

---

## Project Structure

```
CuisineMapProject/
├── backend/
│   ├── app.py                  # Flask app and API routes
│   ├── history_routes.py       # Taste history endpoints
│   ├── history-api.js          # Frontend API client
│   ├── cuisinemap_update.html  # Main app interface
│   └── cuisinemap.db           # SQLite database
├── docs/                       # Project documentation
└── archive/                    # Previous versions
```

---

## Author

Jude Olinmah — built as a full-stack portfolio project, 2026.
