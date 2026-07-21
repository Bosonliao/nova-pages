import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data = json.load(open('data/taoyuan.json','r',encoding='utf-8'))
foods = data.get('food', [])

# Check categories format
yangmei = [f for f in foods if f.get('area') == '楊梅區']
print(f'楊梅區 total: {len(yangmei)}')
if yangmei:
    print(f'First item categories: {yangmei[0].get("categories")}')
    print(f'First item: {json.dumps(yangmei[0], ensure_ascii=False)[:200]}')
    
    # Check all category formats
    cat_set = set()
    for f in yangmei:
        cats = f.get('categories') or []
        for c in cats:
            cat_set.add(c)
    print(f'\nAll categories in 楊梅區: {sorted(cat_set)}')
    
    # Count drinks
    drinks = [f for f in yangmei if any('飲品' in str(c) for c in (f.get('categories') or []))]
    print(f'\n飲品 count: {len(drinks)}')
    
    # Try different match patterns
    for pattern in ['飲品', '飲料', 'drink', '茶']:
        count = sum(1 for f in yangmei if any(pattern in str(c) for c in (f.get('categories') or [])))
        print(f'  "{pattern}" count: {count}')
