import sqlite3
import json
import pandas as pd
import sys
import os

# Connecting our Categorizer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from categorizer import run_ai_categorization

def load_cards_from_db():
    """Fetches ALL columns dynamically from our master database."""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '..', 'database', 'master_cards_final.db')
        
        conn = sqlite3.connect(db_path)
        # CHANGED TO SELECT *: Now we have golf, lounges, fees dynamically!
        query = "SELECT * FROM credit_cards" 
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return None

def calculate_reward_inr(amount, category, card):
    """
    The Core Math Engine: Calculates EXACT Rupee savings.
    Equation: (Amount / Spend Unit) * Category Multiplier * Value of 1 Point in INR
    """
    try:
        spends_unit = float(card['spends_per_reward_unit'])
        inr_value = float(card['unified_reward_value_inr'])
        multipliers = json.loads(card['multipliers_json'])
        
        # Match category (e.g., 'Dining' -> 'dining')
        cat_key = str(category).lower().strip()
        
        # Default multiplier is 1.0 unless a special category matches
        applicable_multiplier = 1.0
        for key, val in multipliers.items():
            if key in cat_key:
                applicable_multiplier = float(val)
                break
                
        # Math calculation
        if spends_unit > 0:
            base_reward_units = amount / spends_unit
            total_inr_saved = base_reward_units * applicable_multiplier * inr_value
            return total_inr_saved
        return 0.0
    except:
        return 0.0

def optimize_spends(transactions_df, cards_df):
    """Finds the absolute best card for every single transaction."""
    optimized_results = []
    total_savings = 0.0
    
    for _, txn in transactions_df.iterrows():
        best_card = "No Recommendation"
        max_saving = -1.0
        
        for _, card in cards_df.iterrows():
            saving = calculate_reward_inr(txn['amount'], txn['category'], card)
            if saving > max_saving:
                max_saving = saving
                best_card = f"{card['bank_name']} {card['card_name']}"
                
        optimized_results.append({
            "Description": str(txn['description'])[:30] + "...", # Trimmed for chat display
            "Amount": txn['amount'],
            "Category": txn['category'],
            "Recommended_Card": best_card,
            "Saved_INR": round(max_saving, 2)
        })
        total_savings += max_saving
        
    return pd.DataFrame(optimized_results), total_savings

def run_chat_environment():
    """The Interactive Chat-Based AI Environment requested by the assignment."""
    print("\n=======================================================")
    print(" 🤖 THE FOUNDING ENGINEER'S AI CREDIT CARD AGENT 🤖")
    print("=======================================================")
    print("Initializing Data Pipelines & Optimization Engines...")
    
    # 1. Run Excel Parsing & Categorization
    test_excel_path = "../../data_samples/transactions.xlsx"
    user_data = run_ai_categorization(test_excel_path)
    
    if user_data is None or user_data.empty:
        print("❌ Could not load or categorize user transactions.")
        return
        
    # 2. Load the Master Database Framework
    cards_data = load_cards_from_db()
    if cards_data is None or cards_data.empty:
        return
        
    # 3. Optimize every single spend!
    print("⚙️ AI Brain is analyzing multiple real-world card T&Cs...")
    opt_df, total_savings = optimize_spends(user_data, cards_data)
    
    print("\n✅ Setup Complete! I am ready.")
    print(f"💰 INITIAL INSIGHT: By routing your spends optimally, you could have saved ₹{total_savings:.2f} this month!")
    
    # 4. THE CHAT LOOP
    while True:
        print("\n-------------------------------------------------------")
        user_input = input("🗣️ You: ").strip().lower()
        
        if user_input in ['exit', 'quit', 'bye', 'close']:
            print("🤖 AI Agent: Goodbye! Keep optimizing your wealth. 🚀")
            break
            
        elif 'save' in user_input or 'total' in user_input or 'savings' in user_input:
            print(f"🤖 AI Agent: Your total mathematically optimized savings are ₹{total_savings:.2f}.")
            print("This is calculated by comparing base rates and category multipliers across all cards in the database.")
            
        elif 'top' in user_input or 'show' in user_input:
            print("🤖 AI Agent: Here are your top 5 optimized transactions showing which card to use:")
            # Sorting to show biggest savings first
            top_5 = opt_df.sort_values(by='Saved_INR', ascending=False).head(5)
            print("\n" + top_5[['Description', 'Category', 'Recommended_Card', 'Saved_INR']].to_string(index=False))
            
        elif 'dining' in user_input:
            dining = opt_df[opt_df['Category'] == 'Dining']
            if not dining.empty:
                best = dining['Recommended_Card'].mode()[0]
                print(f"🤖 AI Agent: You had {len(dining)} dining spends. The most optimized card for your dining habits is {best}.")
            else:
                print("🤖 AI Agent: No dining spends detected in your statement.")
                
        elif 'logic' in user_input or 'how' in user_input:
            print("🤖 AI Agent: I don't guess. I use a Deterministic Math Engine.")
            print("1. I extract your spend category using Regex NLP.")
            print("2. I fetch bank T&Cs (multipliers, point value in INR) from SQLite.")
            print("3. I simulate the transaction across ALL cards and pick the highest yield.")
            
        else:
            print("🤖 AI Agent: I am your financial optimization bot. Ask me about:")
            print("  - 'Total savings'")
            print("  - 'Top spends'")
            print("  - 'Dining / Travel'")
            print("  - 'Your logic'")
            print("Type 'exit' to quit.")

if __name__ == "__main__":
    run_chat_environment()