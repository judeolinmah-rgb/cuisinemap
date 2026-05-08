with open('cuisinemap_update.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

print('File length:', len(content))
print('oignon count:', content.count('oignon'))
print('oignon lowercase count:', content.lower().count('oignon'))
