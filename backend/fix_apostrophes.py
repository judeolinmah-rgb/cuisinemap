with open('cuisinemap_update.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# The ML blocks use curly apostrophe (0x2019) but our injected keys use straight (0x27)
# We need to fix the keys in STATIC_RECIPES to use curly apostrophe

curly = '\u2019'
straight = "'"

fixes = [
    ("Canard \u00e0 l'orange GF \u2014 duck in orange sauce with rice", "Canard \u00e0 l\u2019orange GF \u2014 duck in orange sauce with rice"),
    ("Canard \u00e0 l'orange \u2014 duck in orange sauce dairy-free", "Canard \u00e0 l\u2019orange \u2014 duck in orange sauce dairy-free"),
    ("Canard \u00e0 l'orange \u2014 duck in orange sauce no side", "Canard \u00e0 l\u2019orange \u2014 duck in orange sauce no side"),
    ("Canard \u00e0 l'orange \u2014 roast duck breast in orange sauce", "Canard \u00e0 l\u2019orange \u2014 roast duck breast in orange sauce"),
    ("Gigot d'agneau avec flageolets GF \u2014 leg of lamb GF", "Gigot d\u2019agneau avec flageolets GF \u2014 leg of lamb GF"),
    ("Gigot d'agneau avec haricots verts \u2014 lamb with green beans", "Gigot d\u2019agneau avec haricots verts \u2014 lamb with green beans"),
    ("Gigot d'agneau \u2014 slow-roasted lamb dairy-free", "Gigot d\u2019agneau \u2014 slow-roasted lamb dairy-free"),
    ("Gigot d'agneau \u2014 slow-roasted leg of lamb with flageolet beans", "Gigot d\u2019agneau \u2014 slow-roasted leg of lamb with flageolet beans"),
    ("Jus d'orange avec tartine \u2014 orange juice with toast", "Jus d\u2019orange avec tartine \u2014 orange juice with toast"),
    ("Porridge \u00e0 l'avoine avec fruits \u2014 oat porridge with fruit", "Porridge \u00e0 l\u2019avoine avec fruits \u2014 oat porridge with fruit"),
    ("Soupe \u00e0 l'ail \u2014 garlic and bread soup vegan", "Soupe \u00e0 l\u2019ail \u2014 garlic and bread soup vegan"),
    ("Soupe \u00e0 l'oignon GF sans cro\u00fbton \u2014 onion soup no crouton", "Soupe \u00e0 l\u2019oignon GF sans cro\u00fbton \u2014 onion soup no crouton"),
    ("Soupe \u00e0 l'oignon gratin\u00e9e \u2014 French onion soup with Gruy\u00e8re crouton", "Soupe \u00e0 l\u2019oignon gratin\u00e9e \u2014 French onion soup with Gruy\u00e8re crouton"),
    ("Soupe \u00e0 l'oignon sans cro\u00fbton \u2014 onion soup no crouton", "Soupe \u00e0 l\u2019oignon sans cro\u00fbton \u2014 onion soup no crouton"),
    ("Soupe \u00e0 l'oignon sans fromage \u2014 onion soup dairy-free", "Soupe \u00e0 l\u2019oignon sans fromage \u2014 onion soup dairy-free"),
    ("Soupe \u00e0 l'oignon \u2014 French onion soup with Gruy\u00e8re", "Soupe \u00e0 l\u2019oignon \u2014 French onion soup with Gruy\u00e8re"),
]

count = 0
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"Fixed: {new[:50]}")
        count += 1
    else:
        print(f"NOT FOUND: {old[:50]}")

with open('cuisinemap_update.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nFixed {count} keys. Done!")
