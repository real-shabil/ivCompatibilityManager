# 💊 IV Compatibility Manager v9.1
# Author: Shabil Mohammed Kozhippattil
# Description: Smart hybrid search + colorized JSON builder for IV drug compatibility
# Enhancements: grouped configuration, docstrings, sorted JSON output

import json
import os
import re
from datetime import date
from difflib import get_close_matches
from colorama import Fore, Style, init

META_KEYS = {"schemaVersion", "biDirectional", "compatibilityKeys", "lastUpdate"}


# ------------------ CONFIGURATION ------------------
init(autoreset=True)

FILENAME = "drugInteractions.json"
COMPAT_KEYS = ["solution", "ySite", "syringe", "admixture"]
CHOICES = {"1": "Compatible", "2": "Incompatible", "3": "Variable"}

# ------------------ CORE FILE HANDLING ------------------

def load_data():
    """Load existing JSON file or initialize a new structured dictionary."""
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(Fore.RED + "⚠️  Corrupted JSON file detected. Starting new data.")
    return {
        "schemaVersion": 1.0,
        "biDirectional": True,
        "compatibilityKeys": COMPAT_KEYS,
        "lastUpdate": str(date.today())
    }


def save_data(data):
    """Save JSON data to disk with sorted keys and update last modified date."""
    data["lastUpdate"] = str(date.today())
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)
    print(Fore.GREEN + "✅ Data saved successfully.\n")


# ------------------ SEARCH AND MATCH ------------------

def highlight_match(drug, query):
    """Highlight substring matches in cyan bold for better visibility."""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: Style.BRIGHT + Fore.CYAN + m.group(0) + Style.RESET_ALL, drug)


def get_drug_name(prompt, data):
    """Smart hybrid drug search: partial + fuzzy matching with suggestions."""
    while True:
        name = input(Fore.CYAN + prompt + Style.RESET_ALL).strip()
        if name.lower() == "stop":
            raise KeyboardInterrupt
        if not name:
            print(Fore.RED + "❌ Drug name cannot be empty.")
            continue

        all_drugs = list(data.keys())
        query = name.lower()

        # Case-insensitive substring matches
        substr_matches = [d for d in all_drugs if query in d.lower()]

        if substr_matches:
            print(Fore.YELLOW + "\n💡 Suggestions:")
            for i, match in enumerate(substr_matches[:3], 1):
                print(f"{Fore.YELLOW}{i}. {highlight_match(match, query)}")
            choice = input(
                Fore.GREEN + "Select number or press Enter to keep your input: " + Style.RESET_ALL
            ).strip()
            if choice in ["1", "2", "3"] and int(choice) <= len(substr_matches):
                return substr_matches[int(choice) - 1]

        # Fuzzy fallback if no substring match
        if not substr_matches:
            fuzzy = get_close_matches(name, all_drugs, n=1, cutoff=0.8)
            if fuzzy:
                suggestion = fuzzy[0]
                confirm = input(
                    Fore.YELLOW + f"Did you mean '{suggestion}'? (y/n): " + Style.RESET_ALL
                ).strip().lower()
                if confirm == "y":
                    return suggestion
        return name


# ------------------ COMPATIBILITY ENTRY ------------------

def get_compatibility_values():
    """Prompt user for each compatibility key; map 1–3 or blank to values."""
    compat = {}
    print(Fore.CYAN + "\n⚗️  Enter Compatibility Values (1–3 or Enter = No Data)\n")
    print(Fore.YELLOW + "1 = Compatible   2 = Incompatible   3 = Variable   (Enter = No Data)\n")

    for key in COMPAT_KEYS:
        while True:
            val = input(Fore.GREEN + f"{key.title()}: " + Style.RESET_ALL).strip()
            if val.lower() == "stop":
                raise KeyboardInterrupt
            if not val:
                compat[key] = "No Data"
                break
            elif val in CHOICES:
                compat[key] = CHOICES[val]
                break
            elif val in CHOICES.values():
                compat[key] = val
                break
            else:
                print(Fore.RED + "❌ Invalid entry. Enter 1–3 or press Enter for No Data.")
        print()
    return compat


def generate_auto_note(compat):
    """
    Generate an automated nurse-style note based on the full compatibility pattern.

    compat example:
    {
        "solution": "Compatible" | "Incompatible" | "Variable" | "No Data",
        "ySite":    "Compatible" | "Incompatible" | "Variable" | "No Data",
        "syringe":  "Compatible" | "Incompatible" | "Variable" | "No Data",
        "admixture":"Compatible" | "Incompatible" | "Variable" | "No Data"
    }
    """
    solution = compat.get("solution", "No Data")
    ysite = compat.get("ySite", "No Data")
    syringe = compat.get("syringe", "No Data")
    admixture = compat.get("admixture", "No Data")

    vals = [solution, ysite, syringe, admixture]

    # ------------------------------
    # TIER 1 — Y-site core message
    # ------------------------------
    if all(v == "No Data" for v in vals):
        core = "No compatibility data available — use a dedicated line for safety."
    elif ysite == "Compatible":
        core = "Y-site compatible — co-administration may proceed if no precipitation is observed."
    elif ysite == "Incompatible":
        core = "Y-site incompatible — MUST use a separate line regardless of other routes."
    elif ysite == "Variable":
        core = "Y-site variable — co-administration requires close monitoring for precipitation or color change."
    else:  # ySite = "No Data"
        core = "Y-site data unavailable — prefer a separate line unless other routes strongly support compatibility."

    # ------------------------------
    # TIER 2 — Route-specific modifiers
    # ------------------------------
    modifiers = []

    # Solution
    if solution == "Compatible":
        modifiers.append(
            f"Solution: Compatible — this medication is compatible with {drug_a}."
        )
    elif solution == "Incompatible":
        modifiers.append(
            f"Solution: Incompatible — do not prepare or infuse this medication in {drug_a}."
        )
    elif solution == "Variable":
        modifiers.append(
            f"Solution: Variable — use caution when preparing this medication in {drug_a}."
        )
    elif solution == "No Data":
        modifiers.append(
            f"Solution: No Data — compatibility with {drug_a} is not established."
        )
       
    # Syringe
    if syringe == "Incompatible":
        modifiers.append("Do not mix in syringe due to syringe-level incompatibility.")
    elif syringe == "Variable":
        modifiers.append("Syringe compatibility is variable — avoid direct mixing.")
    elif syringe == "No Data":
        modifiers.append("Syringe compatibility data is unavailable.")

    # Admixture
    if admixture == "Incompatible":
        modifiers.append("Do not combine in admixture due to bag-level incompatibility.")
    elif admixture == "Variable":
        modifiers.append("Admixture data is variable — avoid combining unless clearly indicated.")
    elif admixture == "No Data":
        modifiers.append("Admixture compatibility data is lacking.")

    # ------------------------------
    # TIER 3 — Final summary
    # ------------------------------
    if any(v == "Incompatible" for v in vals):
        summary = "Overall: At least one route is incompatible — separate-line administration is preferred."
    elif all(v == "Compatible" for v in vals):
        summary = "Overall: All available routes show compatibility."
    elif any(v == "Variable" for v in vals):
        summary = "Overall: Mixed or variable evidence — monitor closely if co-administered."
    elif all(v in ["Compatible", "No Data"] for v in vals):
        summary = "Overall: Generally compatible, but missing data warrants caution."
    else:
        summary = "Overall: Limited or mixed information — safest to use a dedicated line."

    # Build final note
    note = core
    if modifiers:
        note += " " + " ".join(modifiers)
    note += " " + summary

    return note


# ------------------ MAIN LOGIC ------------------

def add_entry(data):
    count = len([k for k in data.keys() if k not in META_KEYS])
    print(Fore.MAGENTA + "\n💊 IV Compatibility Manager — Ready")
    print(Fore.YELLOW + f"📦 Currently tracking {count} drugs")
    print(Fore.MAGENTA + "────────────────────────────────────────\n")

    drug_a = get_drug_name("Enter first drug name: ", data)
    print(Fore.YELLOW + f"\n📌 First drug set as: {drug_a}")
    print(Fore.YELLOW + "💡 You can add multiple pairings with this base drug.\n")

    while True:
        drug_b = get_drug_name("Enter second drug name (or 'stop' to exit): ", data)

        compat = get_compatibility_values()
        auto_note = generate_auto_note(compat)
        print(Fore.CYAN + f"\n📝 Auto-generated note:\n{Fore.WHITE}{auto_note}")
        manual = input(Fore.YELLOW + "\nPress Enter to accept or type a custom note: ").strip()
        notes = manual if manual else auto_note
        source = input(Fore.CYAN + "\n📚 Source (default 'Trissel’s Handbook 2025'): ").strip() or "Trissel’s Handbook 2025"

        # Review screen before saving
        print(Fore.MAGENTA + "\n────────────────────────────────────────")
        print("🧾  Review Entry Before Saving")
        print("────────────────────────────────────────")
        print(Fore.CYAN + f"💊 Drug A: {drug_a}")
        print(Fore.CYAN + f"💊 Drug B: {drug_b}\n")
        for k, v in compat.items():
            print(f"{Fore.GREEN}{k.title():<12}{Style.RESET_ALL}: {v}")
        print(f"\n📝 Note: {notes}")
        print(f"📚 Source: {source}")
        print(Fore.MAGENTA + "────────────────────────────────────────")

        confirm = input(Fore.YELLOW + "Confirm and save? (y = yes / e = edit / c = cancel): ").strip().lower()
        if confirm == "stop":
            raise KeyboardInterrupt
        if confirm == "c":
            print(Fore.RED + "❌ Entry cancelled.\n")
            continue
        if confirm == "e":
            print(Fore.YELLOW + "\n🔁 Re-entering compatibility details...\n")
            continue


        if all(v == "No Data" for v in compat.values()):
            compat = {}
        else:
            compat = {k: v for k, v in compat.items() if v != "No Data"}

        entry = {"compatibility": compat, "notes": notes, "source": source}
        data.setdefault(drug_a, {})[drug_b] = entry
        data.setdefault(drug_b, {})[drug_a] = entry
        save_data(data)

        # Shorten long names in display
        base_display = (drug_a[:35] + '…') if len(drug_a) > 40 else drug_a

        cont = input(Fore.CYAN + f"➕ Add another with same {base_display}? (y/n): ").strip().lower()
        if cont != "y":
            print()
            break


def main():
    """Initialize environment and start interactive session."""
    try:
        data = load_data()
        add_entry(data)
    except KeyboardInterrupt:
        print(Fore.RED + "\n🛑 Stopped by user — all safe and saved.\n")


if __name__ == "__main__":
    main()
