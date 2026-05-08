import re

with open('cuisinemap_update.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Handle both normal and escaped quotes in keys
keys1 = set(re.findall(r'"((?:[^"\\]|\\.)+)":\{img:', content))
keys2 = set(re.findall(r"'((?:[^'\\]|\\.)+)':\{img:", content))
keys = keys1 | keys2

# Unescape for comparison
keys_clean = set()
for k in keys:
    keys_clean.add(k.replace("\\'", "'").replace('\\"', '"'))

print(f'Total STATIC_RECIPES entries: {len(keys_clean)}')

# Find all meal names from ML blocks
meals1 = re.findall(r'"((?:[^"\\]|\\.)+)",\d+', content)
meals2 = re.findall(r"'((?:[^'\\]|\\.)+)',\d+", content)
all_meals = set()
for m in meals1 + meals2:
    all_meals.add(m.replace("\\'", "'").replace('\\"', '"'))

missing = [m for m in all_meals if m not in keys_clean]
print(f'Total missing: {len(missing)}')
print()
for m in sorted(missing):
    print(f'  - {m}')
