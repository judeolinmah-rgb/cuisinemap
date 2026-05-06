import sqlite3
import requests
import json
import os
import secrets

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cuisinemap.db")

INTERNATIONAL_CUISINES = [
    "Italian", "Mexican", "Chinese", "Japanese", "Indian",
    "French", "Thai", "Greek", "Spanish", "Moroccan",
    "Turkish", "Vietnamese", "Lebanese", "Jamaican", "Egyptian",
    "Russian", "Polish", "Portuguese", "Malaysian", "Filipino"
]

AMERICAN_CUISINES = [
    {
        "name": "Southern & Soul Food",
        "region": "American",
        "description": "Comfort food rooted in African American culinary tradition.",
        "meals": [
            {"name": "Fried Chicken", "description": "Crispy buttermilk fried chicken.", "ingredients": ["chicken", "buttermilk", "flour", "paprika"]},
            {"name": "Shrimp and Grits", "description": "Creamy grits with seasoned shrimp.", "ingredients": ["shrimp", "grits", "bacon", "butter"]},
            {"name": "Collard Greens", "description": "Slow-cooked greens with ham hock.", "ingredients": ["collard greens", "ham hock", "onion", "garlic"]},
            {"name": "Cornbread", "description": "Golden skillet cornbread.", "ingredients": ["cornmeal", "buttermilk", "eggs", "butter"]},
            {"name": "Macaroni and Cheese", "description": "Baked mac and cheese.", "ingredients": ["macaroni", "cheddar", "milk", "butter"]}
        ]
    },
    {
        "name": "New England",
        "region": "American",
        "description": "Seafood-forward cuisine from the northeastern coast.",
        "meals": [
            {"name": "Clam Chowder", "description": "Creamy chowder with clams and potatoes.", "ingredients": ["clams", "potatoes", "bacon", "cream"]},
            {"name": "Lobster Roll", "description": "Fresh lobster in a buttered roll.", "ingredients": ["lobster", "mayonnaise", "celery", "roll"]},
            {"name": "Boston Baked Beans", "description": "Slow-baked beans with molasses.", "ingredients": ["navy beans", "molasses", "salt pork", "onion"]},
            {"name": "Cod Cakes", "description": "Pan-fried salt cod cakes.", "ingredients": ["salt cod", "potatoes", "parsley", "egg"]},
            {"name": "Cranberry Walnut Stuffing", "description": "Herb stuffing with cranberries.", "ingredients": ["bread", "cranberries", "walnuts", "sage"]}
        ]
    },
    {
        "name": "Louisiana Creole & Cajun",
        "region": "American",
        "description": "Bold cuisine blending French, African, and Native American influences.",
        "meals": [
            {"name": "Gumbo", "description": "Rich stew with sausage and shrimp.", "ingredients": ["andouille", "shrimp", "okra", "roux"]},
            {"name": "Jambalaya", "description": "One-pot rice with chicken and sausage.", "ingredients": ["chicken", "andouille", "rice", "tomatoes"]},
            {"name": "Crawfish Etouffee", "description": "Crawfish in buttery Creole sauce.", "ingredients": ["crawfish", "butter", "onion", "cajun seasoning"]},
            {"name": "Red Beans and Rice", "description": "Slow-cooked red beans with sausage.", "ingredients": ["red beans", "andouille", "onion", "rice"]},
            {"name": "Beignets", "description": "Fried dough with powdered sugar.", "ingredients": ["flour", "yeast", "sugar", "powdered sugar"]}
        ]
    },
    {
        "name": "Tex-Mex & Southwest",
        "region": "American",
        "description": "Bold flavors blending Mexican and American traditions.",
        "meals": [
            {"name": "Beef Fajitas", "description": "Sizzling skirt steak with peppers.", "ingredients": ["skirt steak", "peppers", "onion", "tortillas"]},
            {"name": "Green Chile Enchiladas", "description": "Chicken enchiladas with green chile sauce.", "ingredients": ["chicken", "corn tortillas", "green chiles", "cheese"]},
            {"name": "Texas Chili", "description": "Slow-cooked beef chili with dried chiles.", "ingredients": ["beef chuck", "ancho chiles", "onion", "cumin"]},
            {"name": "Breakfast Tacos", "description": "Scrambled eggs in flour tortillas.", "ingredients": ["eggs", "tortillas", "cheese", "salsa"]},
            {"name": "Fry Bread Tacos", "description": "Crispy fry bread with seasoned beef.", "ingredients": ["flour", "baking powder", "ground beef", "beans"]}
        ]
    },
    {
        "name": "Midwestern",
        "region": "American",
        "description": "Hearty food from America's heartland.",
        "meals": [
            {"name": "Chicago Deep Dish Pizza", "description": "Thick-crust pizza with chunky tomato sauce.", "ingredients": ["pizza dough", "mozzarella", "sausage", "tomatoes"]},
            {"name": "Pork Tenderloin Sandwich", "description": "Breaded fried pork on a bun.", "ingredients": ["pork tenderloin", "breadcrumbs", "egg", "bun"]},
            {"name": "Green Bean Casserole", "description": "Creamy green bean bake.", "ingredients": ["green beans", "mushroom soup", "fried onions", "milk"]},
            {"name": "Beef and Noodle Casserole", "description": "Egg noodles with ground beef.", "ingredients": ["ground beef", "egg noodles", "mushroom soup", "cheddar"]},
            {"name": "Walleye Fish Fry", "description": "Beer-battered walleye fried golden.", "ingredients": ["walleye", "beer", "flour", "old bay"]}
        ]
    },
    {
        "name": "Pacific Northwest",
        "region": "American",
        "description": "Fresh ingredient-driven cuisine from the Pacific coast.",
        "meals": [
            {"name": "Cedar Plank Salmon", "description": "Wild salmon roasted on cedar.", "ingredients": ["salmon", "cedar plank", "lemon", "dill"]},
            {"name": "Dungeness Crab Cakes", "description": "Pan-seared crab cakes.", "ingredients": ["dungeness crab", "breadcrumbs", "egg", "mayonnaise"]},
            {"name": "Salmon Chowder", "description": "Creamy chowder with fresh salmon.", "ingredients": ["salmon", "potatoes", "corn", "cream"]},
            {"name": "Mushroom Risotto", "description": "Creamy risotto with foraged mushrooms.", "ingredients": ["arborio rice", "mushrooms", "parmesan", "white wine"]},
            {"name": "Blackberry Galette", "description": "Rustic tart with fresh blackberries.", "ingredients": ["flour", "butter", "blackberries", "sugar"]}
        ]
    }
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def seed_international_cuisines():
    print("[1] Seeding international cuisines from TheMealDB...")
    with get_db() as conn:
        for cuisine_name in INTERNATIONAL_CUISINES:
            existing = conn.execute(
                "SELECT cuisine_id FROM cuisines WHERE name = ?", (cuisine_name,)
            ).fetchone()
            if existing:
                cuisine_id = existing["cuisine_id"]
                print(f"  - {cuisine_name} already exists")
            else:
                cuisine_id = secrets.token_hex(8)
                conn.execute(
                    "INSERT INTO cuisines (cuisine_id, name, region, description, source) VALUES (?, ?, ?, ?, ?)",
                    (cuisine_id, cuisine_name, "International", f"Traditional {cuisine_name} cuisine", "TheMealDB")
                )
                print(f"  + Added cuisine: {cuisine_name}")
            try:
                url = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={cuisine_name}"
                response = requests.get(url, timeout=10)
                data = response.json()
                if not data.get("meals"):
                    print(f"    No meals found for {cuisine_name}")
                    continue
                meals = data["meals"][:5]
                for meal in meals:
                    existing_meal = conn.execute(
                        "SELECT meal_id FROM meals WHERE name = ? AND cuisine_id = ?",
                        (meal["strMeal"], cuisine_id)
                    ).fetchone()
                    if existing_meal:
                        continue
                    meal_id = secrets.token_hex(8)
                    conn.execute(
                        "INSERT INTO meals (meal_id, cuisine_id, name, description, ingredients, image_url, source) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (meal_id, cuisine_id, meal["strMeal"], f"A traditional {cuisine_name} dish.", json.dumps([]), meal.get("strMealThumb", ""), "TheMealDB")
                    )
                print(f"    Added {len(meals)} meals for {cuisine_name}")
            except Exception as e:
                print(f"    Error fetching {cuisine_name}: {e}")


def seed_american_cuisines():
    print("[2] Seeding regional American cuisines...")
    with get_db() as conn:
        for cuisine_data in AMERICAN_CUISINES:
            existing = conn.execute(
                "SELECT cuisine_id FROM cuisines WHERE name = ?", (cuisine_data["name"],)
            ).fetchone()
            if existing:
                cuisine_id = existing["cuisine_id"]
                print(f"  - {cuisine_data['name']} already exists")
            else:
                cuisine_id = secrets.token_hex(8)
                conn.execute(
                    "INSERT INTO cuisines (cuisine_id, name, region, description, source) VALUES (?, ?, ?, ?, ?)",
                    (cuisine_id, cuisine_data["name"], cuisine_data["region"], cuisine_data["description"], "CuisineMap")
                )
                print(f"  + Added cuisine: {cuisine_data['name']}")
            for meal in cuisine_data["meals"]:
                existing_meal = conn.execute(
                    "SELECT meal_id FROM meals WHERE name = ? AND cuisine_id = ?",
                    (meal["name"], cuisine_id)
                ).fetchone()
                if existing_meal:
                    continue
                meal_id = secrets.token_hex(8)
                conn.execute(
                    "INSERT INTO meals (meal_id, cuisine_id, name, description, ingredients, source) VALUES (?, ?, ?, ?, ?, ?)",
                    (meal_id, cuisine_id, meal["name"], meal["description"], json.dumps(meal["ingredients"]), "CuisineMap")
                )
            print(f"  + Added meals for {cuisine_data['name']}")


if __name__ == "__main__":
    print("CuisineMap Meal Seeder")
    print("=" * 40)
    seed_international_cuisines()
    seed_american_cuisines()
    print("Seeding complete!")
