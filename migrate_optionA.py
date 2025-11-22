import json

FILENAME = "drugInteractions.json"
META_KEYS = {"schemaVersion", "biDirectional", "compatibilityKeys", "lastUpdate"}

with open(FILENAME, "r") as f:
    data = json.load(f)

for drug_a, pairs in data.items():
    if drug_a in META_KEYS or not isinstance(pairs, dict):
        continue

    for drug_b, entry in pairs.items():
        if not isinstance(entry, dict):
            continue

        compat = entry.get("compatibility")
        if not isinstance(compat, dict) or not compat:
            continue

        # Apply Option A cleanup
        values = list(compat.values())
        if values and all(v == "No Data" for v in values):
            compat_clean = {}
        else:
            compat_clean = {k: v for k, v in compat.items() if v != "No Data"}

        entry["compatibility"] = compat_clean

with open(FILENAME, "w") as f:
    json.dump(data, f, indent=4, sort_keys=True)

print("✅ Migration complete: compatibility cleaned according to Option A.")
