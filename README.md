# 💉 IV Compatibility Manager  
A Python-based medical informatics tool that helps nurses and clinicians manage IV drug compatibility safely and efficiently.  
Developed by **Shabil Mohammed Kozhippattil**, RN Hematology/Oncology — KAMC Jeddah.

---

## 🚀 Features

- 🧪 **Search-based IV compatibility lookup**
- 🔄 **Bidirectional compatibility mapping**
- 🧠 **Smart suggestions** when drug names are partially entered
- 📦 **JSON-based structured database** for long-term storage
- ⚠️ **Automatic “No Data” safety notes**
- 📝 **Edit, update, and save compatibility entries**
- 💾 **Clean JSON output** with sorted keys

---

## 📁 Project Structure

ivCompatibilityManager/
│
├── iv-compatibility-manager.py # Main interactive tool
├── drugInteractions.json # Database of IV compatibility
├── migrate_optionA.py # Migration helper for new schema
├── updateNotes.py # Notes updater utility
└── .gitignore # Excludes venv, pycache, etc.


---

## 🖥️ Installation & Setup

### **1. Clone the Repository**

git clone https://github.com/real-shabil/ivCompatibilityManager.git
cd ivCompatibilityManager


### **2. Create a Virtual Environment**
python3 -m venv venv
source venv/bin/activate


### **3. Install Dependencies**   
pip install -r requirements.txt


---

## ▶️ Running the Program

Activate your venv and run:
python iv-compatibility-manager.py


The menu-driven interface will guide you through:

- Adding new drug interactions  
- Updating compatibility records  
- Searching drug compatibility  
- Saving updated JSON files  

---

## 📑 JSON Schema Summary

Each compatibility entry follows this structure:

``` json
{
  "DrugA (IV)": {
    "DrugB (IV)": {
      "compatibility": {
        "solution": "Compatible / Incompatible / No Data",
        "ySite": "Compatible / Incompatible / No Data",
        "syringe": "Compatible / Incompatible / No Data",
        "admixture": "Compatible / Incompatible / No Data"
      },
      "notes": "Clinical note generated or user-added.",
      "source": "Trissel’s Handbook 2025"
    }
  }
}
```

⚠️ Disclaimer
This tool is designed as a clinical decision support aid, not a replacement for:


Official institutional policies


Pharmacy recommendations


Trissel’s IV Compatibility Database


Clinical judgment


Always verify compatibility when administering high-risk medications.

📄 License
This project is licensed under the MIT License.
Feel free to modify and use it for clinical or educational purposes.

👨‍⚕️ Author
Shabil Mohammed Kozhippattil, 
RN Hematology/Oncology — SAUDI ARABIA


GitHub: https://github.com/real-shabil

Passionate about improving patient safety through technology



⭐ Support & Contributions
Issues, suggestions, and contributions are welcome!
Please open an issue or submit a pull request to help improve the tool.

---
