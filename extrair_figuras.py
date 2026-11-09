# -*- coding: utf-8 -*-
"""Extrai do notebook executado as figuras que o gerar_pdf_v2.py usa (fig_*.png)."""
import json, base64, sys
nb = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'analise_forestfires_v2_executado.ipynb', encoding='utf-8'))
names = {1: 'fig_alvo', 7: 'fig_ridge_path', 9: 'fig_residuos', 10: 'fig_hurdle', 11: 'fig_coefs'}
k = 0
for c in nb['cells']:
    for o in c.get('outputs', []):
        if 'data' in o and 'image/png' in o['data']:
            k += 1
            if k in names:
                open(names[k] + '.png', 'wb').write(base64.b64decode(o['data']['image/png']))
                print('ok', names[k])
