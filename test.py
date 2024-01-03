import json

with open('data/dantri_encoding.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# with open('data/dantri_encoding.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, indent=4, ensure_ascii=False)

for key, _ in data.items():
    print(key)