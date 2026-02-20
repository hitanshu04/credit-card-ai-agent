# 💳 AI Credit Card Optimizer
> **A Mathematically Verified Decision Engine for Strategic Financial Routing**

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

---

<img width="1840" height="843" alt="Screenshot 2026-02-21 032746" src="https://github.com/user-attachments/assets/a96d8c99-6b2b-468f-b7bb-e297bb93e054" />

## 🚀 Overview
This agent bypasses LLM hallucinations by using a **Deterministic ROI Engine**. It maps personal transaction data against a verified relational database of T&Cs across 5 major bank providers (HDFC, SBI, ICICI, Axis, Kotak).

---

## ⚙️ System Architecture
The framework follows a **Decoupled 3-Tier Architecture**, ensuring modularity and data integrity.

| Layer | Responsibility | Technology |
| :--- | :--- | :--- |
| **Data Layer** | Relational Knowledge Graph of Card T&Cs | SQLite |
| **Logic Layer** | NLP Heuristics & Deterministic ROI Math | Python (Regex/JSON) |
| **UI Layer** | Reactive Financial Dashboard | Streamlit |

---

## ⚖️ The Mathematical Core
To ensure reliability over "half-baked" predictions, every recommendation is derived using a unified ROI formula:

$$ROI = \left( \frac{\text{Multiplier}}{\text{Spend Unit}} \right) \times \text{Point Value} \times 100$$

> **Note on Mathematical Integrity**: The system currently prioritizes **Verified Baseline Returns (1-2%)**. This is a strategic design choice to maintain data integrity across the framework and avoid the risk of unverified multiplier stacking for specific merchants.

---

## ✨ Key Features
* **📊 Personal Spend Audit**: Scans Excel-based transaction history and identifies exact missed savings.
* **🎯 Smart Intent Routing**: Handles natural language queries for **Lounge Access**, **Golf Privileges**, **Tie-ups (Taj)**, and **Milestones**.
* **⚖️ Fee Waiver Benchmarking**: Specifically filters cards based on `waiver_spend_limit` rather than just initial joining fees.

---

## 🛠️ Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/hitanshu04/credit-card-ai-agent.git
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Run the Application**:
   ```bash
   streamlit run app.py
