import json

INPUT_FILE = "/Users/shabilk/Desktop/Learn_html/pyDrugInteraction/drugInteractions.json"
OUTPUT_FILE = "/Users/shabilk/Desktop/Learn_html/pyDrugInteraction/drugInteractions_updated.json"

COMPAT_KEYS = ["solution", "ySite", "syringe", "admixture"]
META_KEYS = {"schemaVersion", "biDirectional", "compatibilityKeys", "lastUpdate"}


def generate_auto_note(drugAName, compat):
    solution = compat.get("solution", "No Data")
    ySite = compat.get("ySite", "No Data")
    syringe = compat.get("syringe", "No Data")
    admixture = compat.get("admixture", "No Data")

    vals = [solution, ySite, syringe, admixture]
    solutionLabel = drugAName or "this solution"

    # --------------------- TIER 1 — Y-SITE ---------------------
    if all(v == "No Data" for v in vals):
        core = "Y-site data unavailable and all other routes lack information."
    elif ySite == "Compatible":
        core = "Y-site compatible — co-administer if no precipitation is observed."
    elif ySite == "Incompatible":
        core = "Y-site incompatible — MUST use a separate line regardless of other routes."
    elif ySite == "Variable":
        core = "Y-site variable — requires close monitoring for precipitation or color change."
    else:
        core = "Y-site data unavailable — prefer separate line unless other routes show strong compatibility."

    # --------------------- TIER 2 — MODIFIERS ---------------------
    modifiers = []

    # Solution
    if solution == "Compatible":
        modifiers.append(
            f"Solution: Compatible — this medication is compatible with {solutionLabel}."
        )
    elif solution == "Incompatible":
        modifiers.append(
            f"Solution: Incompatible — do not prepare or infuse this medication in {solutionLabel}."
        )
    elif solution == "Variable":
        modifiers.append(
            f"Solution: Variable — use caution when preparing this medication in {solutionLabel}."
        )
    elif solution == "No Data":
        modifiers.append(
            f"Solution: No Data — compatibility with {solutionLabel} is not established."
        )

    # Syringe
    if syringe == "Incompatible":
        modifiers.append("Do not mix in syringe due to syringe incompatibility.")
    elif syringe == "Variable":
        modifiers.append("Syringe compatibility is variable — avoid direct mixing.")
    elif syringe == "No Data":
        modifiers.append("Syringe compatibility data is unavailable.")

    # Admixture
    if admixture == "Incompatible":
        modifiers.append("Admixture incompatible — do not combine in the same IV bag.")
    elif admixture == "Variable":
        modifiers.append("Admixture data is variable — avoid combining.")
    elif admixture == "No Data":
        modifiers.append("Admixture compatibility data is lacking.")

    # --------------------- TIER 3 — SUMMARY ---------------------
    if "Incompatible" in vals:
        summary = (
            "Overall: At least one route is incompatible — separate line preferred."
        )
    elif all(v == "Compatible" for v in vals):
        summary = "Overall: All data supports compatibility."
    elif "Variable" in vals:
        summary = "Overall: Mixed or variable data — monitor closely."
    elif all(v in ["Compatible", "No Data"] for v in vals):
        summary = "Overall: Generally compatible but missing data warrants caution."
    else:
        summary = (
            "Overall: Limited or mixed evidence — safest to use a dedicated line."
        )

    return f"{core} { ' '.join(modifiers) } {summary}"


# --------------------- MAIN PROCESSOR ---------------------
with open(INPUT_FILE, "r") as f:
    data = json.load(f)

for drugA, pairs in list(data.items()):
    if drugA in META_KEYS:
        continue

    for drugB, entry in pairs.items():
        compat = entry.get("compatibility", {})

        # EMPTY {} means All No Data
        if not compat:
            compat = {
                "solution": "No Data",
                "ySite": "No Data",
                "syringe": "No Data",
                "admixture": "No Data",
            }

        # Regenerate note
        new_note = generate_auto_note(drugA, compat)

        # Save back
        entry["notes"] = new_note

# Write out cleaned file
with open(OUTPUT_FILE, "w") as f:
    json.dump(data, f, indent=4)

print("✅ Updated JSON saved to:", OUTPUT_FILE)
