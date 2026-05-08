with open('cuisinemap_update.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the soupe entry
idx = content.find('Soupe')
while idx != -1:
    snippet = content[idx:idx+200]
    if 'oignon' in snippet.lower():
        print(repr(snippet[:150]))
        print('---')
    idx = content.find('Soupe', idx+1)
    if idx > 5000000:
        break
