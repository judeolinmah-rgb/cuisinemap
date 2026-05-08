with open('cuisinemap_update.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

print("File length before:", len(content))

# The inject_missing.py inserted recipes before // ── FRENCH MISSING ──
# which was inside STATIC_RECIPES - but let's verify the recipes ARE in STATIC_RECIPES
# by checking for the Buddha recipe entry

if '"Buddha\'s delight":{img:' in content or '"Buddha\u2019s delight":{img:' in content:
    print("Buddha recipe found in STATIC_RECIPES - good")
else:
    print("Buddha recipe NOT in STATIC_RECIPES - need to check")

# Find what's around FRENCH MISSING
idx = content.find('FRENCH MISSING')
print("\nContext around FRENCH MISSING:")
print(repr(content[max(0,idx-300):idx+100]))
