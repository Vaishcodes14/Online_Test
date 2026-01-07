import json

with open("data/english.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("✅ JSON is valid")
print("Total questions:", len(data))
