with open('cuisinemap_update.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

sr_idx = content.find('var STATIC_RECIPES')

# Find the injected block - it starts with a newline and recipe entries
# The inject script inserted new_recipes string before FRENCH MISSING
# Let's find what's between position 150000 and 160000 that looks wrong

# Find the exact injection - look for img: before STATIC_RECIPES
img_positions = []
idx = 0
while True:
    idx = content.find('{img:', idx)
    if idx == -1 or idx > sr_idx:
        break
    img_positions.append(idx)
    idx += 1

print(f"Found {len(img_positions)} {{img: occurrences before STATIC_RECIPES")
if img_positions:
    for pos in img_positions[:5]:
        print(f"\nPosition {pos}:")
        print(repr(content[max(0,pos-100):pos+50]))
