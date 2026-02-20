import pandas as pd
import sys
import os
import re

# Sys path hack so we can import our parser from another folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from parsers.excel_parser import parse_user_transactions

def categorize_transaction(description):
    """
    Advanced Local NLP Engine with Word Boundary Regex.
    Prevents 'GOLA' from being categorized as 'OLA' (Travel).
    """
    desc = str(description).upper()

    categories = {
        "Travel": ["IRCTC", "MAKE MY TRIP", "MMT", "UBER", "OLA", "INDIGO", "FLIGHT", "FASTAG", "RAPIDO"],
        "Dining": ["ZOMATO", "SWIGGY", "MCDONALDS", "KFC", "STARBUCKS", "CAFE", "RESTAURANT", "DOMINOS", "GOLA", "SUNBURN"],
        "Groceries": ["BLINKIT", "ZEPTO", "INSTAMART", "BIGBASKET", "DMART", "RELIANCE SMART", "GROFERS"],
        "Shopping": ["AMAZON", "FLIPKART", "MYNTRA", "AJIO", "ZARA", "SHOPPERS STOP", "CHUMBAK", "ZETWERK"],
        "Utilities": ["BESCOM", "AIRTEL", "JIO", "RECHARGE", "BILL", "ELECTRICITY", "BWSSB", "CRED"],
        "Health": ["PHARMACY", "APOLLO", "HOSPITAL", "CLINIC", "PHYSIO", "1MG", "PRACTO"],
        "Fuel": ["PETROL", "HPCL", "BPCL", "INDIAN OIL", "SHELL", "FUEL"],
        "Investment": ["MUTUAL FUND", "SIP", "ZERODHA", "GROWW", "PPFAS", "HDFCMF", "BSE", "NSE"]
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            # The Senior Fix: \b ensures we only match whole words!
            # \W+ matches non-word characters (like hyphens in UPI-OLA)
            pattern = rf"\b{keyword}\b"
            # We replace hyphens and dots with spaces so the regex boundary works perfectly on UPI notes
            clean_desc = desc.replace("-", " ").replace(".", " ")
            if re.search(pattern, clean_desc):
                return category
                
    return "Retail/Others"


def run_ai_categorization(file_path):
    """
    Takes the raw Excel file, parses it, and adds the smart categories.
    """
    print("🧠 Starting Local NLP Engine...")
    
    # 1. Get clean data from our parser
    df = parse_user_transactions(file_path)
    
    if df is None or df.empty:
        print("❌ No data to categorize.")
        return None

    # 2. Apply our 'AI' Brain to every single row!
    print("⏳ Categorizing 101 transactions... Please wait.")
    df['category'] = df['description'].apply(categorize_transaction)
    
    print("✅ Categorization Complete!")
    return df

if __name__ == "__main__":
    # Test path
    test_file = "../../data_samples/transactions.xlsx"
    
    categorized_data = run_ai_categorization(test_file)
    
    if categorized_data is not None:
        print("\n--- Top 10 Categorized Spends ---")
        # Showing the Description and the NEW Category we just generated
        print(categorized_data[['description', 'amount', 'category']].head(10))
        
        # Bonus: Show how much money went into each category!
        print("\n--- Total Spends by Category ---")
        print(categorized_data.groupby('category')['amount'].sum())