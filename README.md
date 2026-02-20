💳 AI Credit Card Optimizer
A Mathematically Verified Financial Intelligence Agent


🚀 Overview
This project is a production-grade AI agent designed to optimize personal financial routing across 5 major bank providers (HDFC, SBI, ICICI, Axis, Kotak). It analyzes personal transaction statements and recommends the mathematically optimal card for maximum ROI.


🛠️ Architecture
The system follows a Decoupled 3-Tier Architecture:

Data Layer: Relational SQLite database storing verified credit card T&Cs (multipliers, fees, perks).

Logic Layer (NLP Heuristics): An intent-routing engine that maps user queries to deterministic mathematical models.

UI Layer: A reactive Streamlit dashboard for real-time spend auditing.


⚖️ Mathematical Model
To ensure Quality over Hallucination, every recommendation is derived using a deterministic ROI formula:



Note: For this iteration, the system prioritizes Conservative Baseline Returns (1-2%) to ensure data integrity across the framework, avoiding the risks of unverified multiplier stacking.


✨ Key Features
Personal Spend Audit: Automatically highlights missed savings from Excel transaction statements.

Comprehensive Benchmarking: Covers all 5 bank providers across sub-points like Lounge access, Golf privileges, Special Tie-ups (Taj), and Reward Expiry.

Sorted Optimization Table: Displays top savings opportunities in a clean, high-to-low sorted interface.