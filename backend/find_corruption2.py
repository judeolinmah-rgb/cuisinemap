with open('cuisinemap_update.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

sr_idx = content.find('var STATIC_RECIPES')

# Show content around position 150000-155000 where Buddha was found
chunk = content[150800:151200]
print("Around Buddha position:")
print(repr(chunk))
print()

# Also check if there's a large block of injected text
# by looking for the new_recipes marker
markers = [
    "Canard \u00e0 l'orange GF",
    "Buddha's delight",
    "Fett'unta",
    "Labneh with za'atar",
]
for m in markers:
    idx = content.find(m)
    if idx != -1 and idx < sr_idx:
        print(f"FOUND IN ML BLOCKS: '{m}' at position {idx}")
        print(repr(content[max(0,idx-50):idx+100]))
        print()
