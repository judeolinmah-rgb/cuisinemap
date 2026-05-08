with open('cuisinemap_update.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Find Buddha's delight in context
idx = content.find("Buddha")
while idx != -1:
    start = max(0, idx - 200)
    end = min(len(content), idx + 200)
    print(repr(content[start:end]))
    print('---')
    idx = content.find("Buddha", idx + 1)
