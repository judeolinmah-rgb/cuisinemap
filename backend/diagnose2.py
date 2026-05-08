with open('cuisinemap_update.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find where the injected content landed in ML blocks
# Look for recipe-like content (with {img: inside ML blocks
# The ML blocks should only contain C([...]) arrays

# Find the start of STATIC_RECIPES
sr_idx = content.find('var STATIC_RECIPES')
print("STATIC_RECIPES starts at:", sr_idx)

# Find Buddha in ML (before STATIC_RECIPES)
buddha_idx = content.find("Buddha")
print("Buddha first appears at:", buddha_idx)
print("Is Buddha in ML blocks (before STATIC_RECIPES)?", buddha_idx < sr_idx)

# Show context around first Buddha
print("\nContext:")
print(repr(content[max(0,buddha_idx-100):buddha_idx+100]))
