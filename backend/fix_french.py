with open('cuisinemap_update.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'see Soupe a l oignon recipe \u2014 with Gruyere gratin',
    '6 large onions sliced","1 litre beef stock","1 cup white wine","3 tbsp butter","thyme","bay leaf","4 baguette slices","150g Gruyere grated'
)

content = content.replace(
    'Make French onion soup. Top with baguette and gruyere. Grill until bubbling.',
    'Caramelise onions in butter 45 minutes until golden.","Add wine and reduce.","Add stock and herbs, simmer 20 minutes.","Season well.","Top with baguette and Gruyere, grill until bubbling.'
)

content = content.replace(
    'see Soupe a l oignon recipe \u2014 serve without crouton',
    '6 large onions sliced","1 litre beef stock","1 cup white wine","3 tbsp butter","thyme","bay leaf","salt and pepper'
)

content = content.replace(
    'Make French onion soup. Serve without the bread for a GF version.',
    'Caramelise onions in butter 45 minutes.","Add wine and reduce.","Add stock and herbs, simmer 20 minutes.","Season well.","Serve without crouton for GF version.'
)

content = content.replace(
    'see Soupe a l oignon recipe \u2014 without crouton',
    '6 large onions sliced","1 litre beef stock","1 cup white wine","3 tbsp butter","thyme","bay leaf","salt and pepper'
)

content = content.replace(
    'Make French onion soup. Serve without bread.',
    'Caramelise onions in butter 45 minutes.","Add wine and reduce.","Add stock and herbs, simmer 20 minutes.","Season well.","Serve without crouton.'
)

content = content.replace(
    'see Soupe a l oignon recipe \u2014 dairy-free',
    '6 large onions sliced","1 litre vegetable stock","1 cup white wine","3 tbsp olive oil","thyme","bay leaf","salt and pepper","baguette slices'
)

content = content.replace(
    'see Soupe a l oignon recipe',
    '6 large onions sliced","1 litre beef stock","1 cup white wine","3 tbsp butter","thyme","bay leaf","4 baguette slices","150g Gruyere grated'
)

content = content.replace(
    'See Soupe a l oignon for the full recipe.',
    'Caramelise onions in butter 45 minutes.","Add wine and reduce.","Add stock and herbs, simmer 20 minutes.","Season well.","Top with baguette and Gruyere, grill until bubbling.'
)

content = content.replace(
    'see Canard a l orange recipe \u2014 naturally gluten-free',
    'juice of 3 oranges","zest of 1 orange","2 duck breasts","2 tbsp honey","1 cup chicken stock","thyme","salt and pepper'
)

content = content.replace(
    'Make Canard a l orange. All ingredients are naturally gluten-free.',
    'Score duck skin and season.","Render skin side down 12 minutes until crispy.","Flip and cook 5 minutes, rest.","Reduce orange juice, zest, honey and stock into glossy sauce.","Slice duck and serve with orange sauce.'
)

content = content.replace(
    'see Canard a l orange recipe',
    'juice of 3 oranges","zest of 1 orange","2 duck breasts","2 tbsp honey","1 cup chicken stock","thyme","salt and pepper'
)

content = content.replace(
    'See Canard a l orange for the full recipe.',
    'Score duck skin and season generously.","Render skin side down 12 minutes until very crispy.","Flip and cook 5 minutes then rest 10 minutes.","Reduce orange juice, zest, honey and stock into glossy sauce.","Slice duck and serve with orange sauce.'
)

content = content.replace(
    'see Gigot d agneau recipe \u2014 naturally gluten-free',
    '1 leg of lamb","8 cloves garlic","fresh rosemary","4 tbsp olive oil","400g flageolet beans","salt and pepper'
)

content = content.replace(
    'Make Gigot d agneau. Serve with flageolet beans \u2014 naturally gluten-free.',
    'Stud lamb with garlic and rosemary.","Rub with olive oil and season.","Roast at 200C for 20 minutes then 180C for 1 hour.","Rest 15 minutes.","Serve with warm flageolet beans.'
)

content = content.replace(
    'see Gigot d agneau recipe',
    '1 whole leg of lamb","8 cloves garlic","fresh rosemary","4 tbsp olive oil","1 cup white wine","salt and pepper'
)

content = content.replace(
    'See Gigot d agneau for the full recipe.',
    'Stud lamb with garlic and rosemary.","Rub with olive oil and season generously.","Roast at 200C for 20 minutes then 160C for 2 hours.","Rest 20 minutes.","Carve and serve with pan juices.'
)

with open('cuisinemap_update.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! All French placeholder recipes updated.")
