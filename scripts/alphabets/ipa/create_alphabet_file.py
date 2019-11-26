import os
import json

dir_path = os.path.dirname(__file__)
in_path = os.path.join(dir_path, 'symbols_unicode.json')
out_path = os.path.join(dir_path, 'alphabet.json')

# Load ipa symbols
with open(in_path, 'r') as f:
    data = json.load(f)

# Create alphabet format
symbols = {}

for k, v in data.items():
    for code in v:
        char = chr(int(code, 16))

        symbols[char] = {
            'hex': code
        }

out_data = {
    'symbols': symbols,
    'normalizations': {
        'ɡ': ['g'],
    }
}

# Write
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out_data, f, indent=4, ensure_ascii=False)
