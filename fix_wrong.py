# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('data-zh.json','r',encoding='utf-8'))
foods = data['台北']['food']
bad_indices = [295, 305, 313, 315, 355, 356, 358, 359, 360, 361, 363, 364, 365, 367, 368, 369, 370, 371]
for i in bad_indices:
    if 'dishes' in foods[i]:
        nm = foods[i].get('name','?')[:30]
        del foods[i]['dishes']
        print(f'Cleared dishes from idx={i}: {nm}')
with open('data-zh.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f'\nRemoved wrong dishes from {len(bad_indices)} restaurants')