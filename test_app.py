from app import handle_query

queries = [
    ('vintage graphic tee under $30', 'Example wardrobe'),
    ('vintage graphic tee under $30', 'Empty wardrobe (new user)'),
    ('designer ballgown size XXS under $5', 'Example wardrobe'),
    ('', 'Example wardrobe'),
]

print('=' * 60)
print('TESTING APP.HANDLE_QUERY')
print('=' * 60)
print()

for query, wardrobe_choice in queries:
    print(f'--- Query: "{query}" | Wardrobe: {wardrobe_choice} ---')
    result = handle_query(query, wardrobe_choice)
    
    print(f'Listing:   {result[0][:100]}{"..." if len(result[0]) > 100 else ""}')
    print(f'Outfit:    {result[1][:100]}{"..." if result[1] and len(result[1]) > 100 else ""}')
    print(f'Fit Card:  {result[2][:100]}{"..." if result[2] and len(result[2]) > 100 else ""}')
    print()