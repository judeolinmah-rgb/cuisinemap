with open('cuisinemap_update.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find the French missing section we pasted
idx = content.find('FRENCH MISSING')
if idx == -1:
    print('French missing comment not found')
else:
    print('Found French missing section')
    print(repr(content[idx:idx+500]))
