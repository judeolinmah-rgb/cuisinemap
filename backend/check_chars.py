with open('cuisinemap_update.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find Canard in ML blocks
idx = content.find("Canard")
while idx != -1:
    snippet = content[idx:idx+80]
    if 'orange' in snippet:
        print("Found:", repr(snippet))
        print("Char codes:", [hex(ord(c)) for c in snippet[:30]])
        print('---')
    idx = content.find("Canard", idx+1)
    if idx > 5000000:
        break
