import os
import json

dir_path = os.path.dirname(__file__)
in_path = os.path.join(dir_path, 'symbols.json')
out_path = os.path.join(dir_path, 'alphabet.json')

# Load symbols
with open(in_path, 'r') as f:
    data = json.load(f)

# Convert to alphabet format
symbols = {}

for group_name, group_symbols in data['symbols'].items():
    for s, info in group_symbols.items():
        symbols[s] = info

out_data = {
    'symbols': symbols,
    'normalizations': data['normalizations'],
}

# Save as alphabet json
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out_data, f, indent=4, ensure_ascii=False)
