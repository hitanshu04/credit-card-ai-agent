import streamlit as st
import pandas as pd
import sys
import os
import json
import re

# --- ARCHITECTURE LINKING ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ai_engine')))
from ai_engine.categorizer import run_ai_categorization
from ai_engine.chat_agent import load_cards_from_db, optimize_spends

# --- 1. UI CONFIG ---
st.set_page_config(page_title="AI Card Optimizer Pro", page_icon="💳", layout="wide")
st.title("💳 AI Credit Card Optimizer")
st.markdown("*A Data-Driven Decision Engine for Personal Finance Optimization*")

# --- 2. THE DATA PIPELINE (100% Live Sync) ---
@st.cache_data
def load_and_verify_data():
    try:
        excel_path = "../data_samples/transactions.xlsx"
        user_data = run_ai_categorization(excel_path)
        cards_data = load_cards_from_db()
        if user_data is not None and cards_data is not None:
            opt_df, total_savings = optimize_spends(user_data, cards_data)
            opt_df = opt_df.rename(columns={'Saved_INR': 'Potential_Savings_INR'})
            return opt_df, total_savings, cards_data
        return None, 0.0, None
    except Exception as e:
        st.error(f"Data Sync Failed: {e}")
        return None, 0.0, None

opt_df, total_savings, full_cards_db = load_and_verify_data()

# --- 3. SIDEBAR (Personalized Audit) ---
with st.sidebar:
    st.header("📊 Spending Insights")
    if opt_df is not None:
        st.success(f"**Potential Savings: ₹{total_savings:.2f}**")
        summary = opt_df.groupby('Category')['Potential_Savings_INR'].sum().reset_index()
        st.dataframe(summary.sort_values(by='Potential_Savings_INR', ascending=False), hide_index=True)

# --- 4. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "I am connected to the 5-bank provider framework. Ask me about **'missed savings'**, **'expiry'**, **'golf'**, **'taj tie-ups'**, or **'international travel'**."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- 5. THE GLOBAL OPTIMIZATION ENGINE ---
if prompt := st.chat_input("Query the framework..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        p = prompt.lower()
        response = ""
        
        # CATEGORY 1: Spend Optimization (Highlighting spends with clean UI)
        if any(x in p for x in ['optimize', 'highlight', 'missed', 'past']):
            response = "I have scanned your personal transactions and mapped them to the best available cards to maximize ROI:"
            st.markdown(response)
            if opt_df is not None:
                # Fixed: Sorting by savings and clean indexing
                clean_table = opt_df.sort_values(by='Potential_Savings_INR', ascending=False).head(10).reset_index(drop=True)
                clean_table.index += 1
                st.table(clean_table[['Category', 'Amount', 'Recommended_Card', 'Potential_Savings_INR']])

        # CATEGORY 2: The Universal DB Benchmarking (A-Z Coverage)
        else:
            def universal_query_engine(intent, df):
                if df is None: return "Database Error."
                
                # A. PERK MAPPING (Covering all sub-points from doc)
                perk_logic = {
                    'network': ('network', 'Card Network (Visa/MC/Amex)'),
                    'golf': ('perk_golf', 'Golf Privileges'),
                    'movie': ('perk_movies', 'Movie Benefits'),
                    'lounge': ('lounge_domestic', 'Lounge Access (Domestic/Intl)'),
                    'longue': ('lounge_domestic', 'Lounge Access'), # Typo handle
                    'expiry': ('reward_expiry_months', 'Reward Expiry Rules'),
                    'expire': ('reward_expiry_months', 'Reward Expiry Rules'),
                    'taj': ('benefit_special_tieups', 'Taj/Special Tie-ups'),
                    'tie': ('benefit_special_tieups', 'Special Brand Tie-ups'),
                    'milestone': ('benefit_milestones', 'Milestone Benefits'),
                    'miletsone': ('benefit_milestones', 'Milestone Benefits'), # Typo handle
                    'welcome': ('benefit_welcome', 'Welcome Benefits'),
                    'wlecome': ('benefit_welcome', 'Welcome Benefits'), # Typo handle
                    'other': ('perk_others', 'Miscellaneous Benefits')
                }
                
                # Priority 1: Check if user is asking for a Perk
                for key, (col, title) in perk_logic.items():
                    if key in intent:
                        # Scan ALL cards and filter valid ones
                        matches = df[~df[col].astype(str).str.contains('(?i)no|none', regex=True)]
                        if not matches.empty:
                            res = f"✨ **Database Results for {title}:**\n\n"
                            for _, row in matches.iterrows():
                                res += f"- **{row['bank_name']} {row['card_name']}**: {row[col]}\n"
                            return res

                # Priority 2: Check for Fees & Waivers (Requirement Met)
                if any(x in intent for x in ['waive', 'waiver', 'less spend', 'waiver limit']):
                    valid = df[df['waiver_spend_limit'] > 0].sort_values(by='waiver_spend_limit')
                    res = "⚖️ **Spend-based Fee Waivers (Lowest First):**\n\n"
                    for _, row in valid.iterrows():
                        res += f"- **{row['bank_name']} {row['card_name']}**: Waived at ₹{row['waiver_spend_limit']:,.0f} annual spend.\n"
                    return res
                if 'renewal' in intent or 'renwal' in intent:
                    best = df.loc[df['renewal_fee'].idxmin()]
                    return f"🔄 For the lowest **Renewal Fee**, the **{best['bank_name']} {best['card_name']}** is the winner at ₹{best['renewal_fee']}."
                if any(x in intent for x in ['fee', 'joining', 'cheap', 'free']):
                    best = df.loc[df['joining_fee'].idxmin()]
                    return f"💰 For the lowest **Joining Fee**, the **{best['bank_name']} {best['card_name']}** is optimal at ₹{best['joining_fee']}."

                # Priority 3: The Universal ROI Math Engine (Dining, Travel, Utilities, Reward System)
                cat_map = {
                    'dining': ['dining', 'food', 'dinig'],
                    'international': ['international', 'abroad', 'foreign', 'intetnational'],
                    'domestic': ['domestic', 'india', 'local'],
                    'travel': ['travel', 'trip', 'flight'],
                    'utilities': ['utility', 'utilities', 'bill'],
                    'shopping': ['shopping', 'amazon', 'online', 'reward system', 'highest reward']
                }
                target = next((k for k, v in cat_map.items() if any(word in intent for word in v)), None)
                
                if target or 'reward' in intent:
                    target_cat = target or 'shopping' # Default to shopping if general reward asked
                    best_card, max_roi = None, -1.0
                    
                    for _, row in df.iterrows():
                        try:
                            m_json = json.loads(row['multipliers_json'])
                            # Math ROI Formula Calculation
                            mult = m_json.get(target_cat, m_json.get('travel' if 'travel' in str(target_cat) else '', 1.0))
                            unit = float(row['spends_per_reward_unit']) or 100
                            roi = (float(mult) / unit) * float(row['unified_reward_value_inr']) * 100
                            
                            if roi > max_roi:
                                max_roi, best_card = roi, row
                        except: continue
                    
                    if best_card is not None:
                        return f"📈 **Mathematical Winner for {target_cat.capitalize()}:** The **{best_card['bank_name']} {best_card['card_name']}** offers a return of **{max_roi:.2f}%**."

                return "🤖 I can analyze cards for 'Movies', 'Golf', 'Taj tie-ups', 'Waivers', or 'Travel'. Specify a category to query."

            response = universal_query_engine(p, full_cards_db)
            st.markdown(response)

        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})


# import streamlit as st
# import pandas as pd
# import sys
# import os
# import json
# import re

# # --- ARCHITECTURE LINKING ---
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ai_engine')))
# from ai_engine.categorizer import run_ai_categorization
# from ai_engine.chat_agent import load_cards_from_db, optimize_spends

# # --- 1. UI CONFIG ---
# st.set_page_config(page_title="AI Card Optimizer Pro", page_icon="💳", layout="wide")
# st.title("💳 AI Credit Card Optimizer")
# st.markdown("*Mathematically Verified Framework | RVITM Final Submission Version*")

# # --- 2. DATA PIPELINE (Cached) ---
# @st.cache_data
# def load_and_verify_data():
#     try:
#         excel_path = "../data_samples/transactions.xlsx"
#         user_data = run_ai_categorization(excel_path)
#         cards_data = load_cards_from_db()
#         if user_data is not None and cards_data is not None:
#             opt_df, total_savings = optimize_spends(user_data, cards_data)
#             opt_df = opt_df.rename(columns={'Saved_INR': 'Potential_Savings_INR'})
#             return opt_df, total_savings, cards_data
#         return None, 0.0, None
#     except Exception as e:
#         st.error(f"Data Sync Failed: {e}")
#         return None, 0.0, None

# opt_df, total_savings, full_cards_db = load_and_verify_data()

# # --- 3. SIDEBAR ---
# with st.sidebar:
#     st.header("📊 Spending Insights")
#     if opt_df is not None:
#         st.success(f"**Potential Savings: ₹{total_savings:.2f}**")
#         summary = opt_df.groupby('Category')['Potential_Savings_INR'].sum().reset_index()
#         st.dataframe(summary.sort_values(by='Potential_Savings_INR', ascending=False), hide_index=True)

# # --- 4. CHAT INTERFACE ---
# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "assistant", "content": "I am ready. Ask about **'missed savings'**, **'expiry'**, **'golf'**, **'taj tie-ups'**, or the best card for any spend category."}]

# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]): st.markdown(msg["content"])

# # --- 5. THE GLOBAL OPTIMIZATION ENGINE ---
# if prompt := st.chat_input("Query the framework..."):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"): st.markdown(prompt)

#     with st.chat_message("assistant"):
#         p = prompt.lower()
#         response = ""
        
#         # CATEGORY 1: Spend Optimization
#         if any(x in p for x in ['optimize', 'highlight', 'missed', 'past']):
#             response = "I have analyzed your transactions. Here are the top spends where routing to the recommended card would maximize your ROI:"
#             st.markdown(response)
#             if opt_df is not None:
#                 clean_table = opt_df.sort_values(by='Potential_Savings_INR', ascending=False).head(10).reset_index(drop=True)
#                 clean_table.index += 1
#                 st.table(clean_table[['Category', 'Amount', 'Recommended_Card', 'Potential_Savings_INR']])

#         # CATEGORY 2: Universal Benchmarking
#         else:
#             def universal_query_engine(intent, df):
#                 if df is None: return "Database Error."
                
#                 # A. PERK MAPPING
#                 perk_logic = {
#                     'network': ('network', 'Card Network'),
#                     'golf': ('perk_golf', 'Golf Privileges'),
#                     'movie': ('perk_movies', 'Movie Benefits'),
#                     'lounge': ('lounge_domestic', 'Lounge Access'),
#                     'longue': ('lounge_domestic', 'Lounge Access'),
#                     'expiry': ('reward_expiry_months', 'Reward Expiry'),
#                     'taj': ('benefit_special_tieups', 'Taj/Special Tie-ups'),
#                     'tie': ('benefit_special_tieups', 'Special Brand Tie-ups'),
#                     'milestone': ('benefit_milestones', 'Milestone Benefits'),
#                     'welcome': ('benefit_welcome', 'Welcome Benefits')
#                 }
                
#                 for key, (col, title) in perk_logic.items():
#                     if key in intent:
#                         matches = df[~df[col].astype(str).str.contains('(?i)no|none', regex=True)]
#                         if not matches.empty:
#                             res = f"✨ **Database Analysis for {title}:**\n\n"
#                             for _, row in matches.iterrows():
#                                 res += f"- **{row['bank_name']} {row['card_name']}**: {row[col]}\n"
#                             return res

#                 # B. FEES & WAIVERS
#                 if any(x in intent for x in ['waive', 'waiver', 'spend to get fee']):
#                     valid = df[df['waiver_spend_limit'] > 0].sort_values(by='waiver_spend_limit')
#                     res = "⚖️ **Spend-based Fee Waivers (Lowest First):**\n\n"
#                     for _, row in valid.iterrows():
#                         res += f"- **{row['bank_name']} {row['card_name']}**: Waived on ₹{row['waiver_spend_limit']:,.0f} spend.\n"
#                     return res
#                 if 'renewal' in intent or 'renwal' in intent:
#                     best = df.loc[df['renewal_fee'].idxmin()]
#                     return f"🔄 Lowest **Renewal Fee**: **{best['bank_name']} {best['card_name']}** at ₹{best['renewal_fee']}."
#                 if any(x in intent for x in ['fee', 'joining', 'cheap', 'free']):
#                     best = df.loc[df['joining_fee'].idxmin()]
#                     return f"💰 Lowest **Joining Fee**: **{best['bank_name']} {best['card_name']}** at ₹{best['joining_fee']}."

#                 # C. ROI MATH ENGINE (FIXED FOR INTERNATIONAL/DOMESTIC)
#                 cat_map = {
#                     'dining': ['dining', 'food', 'dinig'],
#                     'international': ['international', 'abroad', 'foreign'],
#                     'domestic': ['domestic', 'india', 'local'],
#                     'travel': ['travel', 'trip', 'flight'],
#                     'utilities': ['utility', 'utilities', 'bill'],
#                     'shopping': ['shopping', 'amazon', 'online']
#                 }
#                 target = next((k for k, v in cat_map.items() if any(word in intent for word in v)), None)
                
#                 if target or 'reward' in intent:
#                     target_cat = target or 'shopping'
#                     best_card, max_roi = None, -1.0
#                     for _, row in df.iterrows():
#                         try:
#                             m_json = json.loads(row['multipliers_json'])
#                             # THE FIX: Priority fetch for Int/Dom categories from travel multipliers
#                             mult = m_json.get(target_cat)
#                             if mult is None:
#                                 # Fallback to 'travel' multiplier if specific dom/int not found
#                                 if target_cat in ['domestic', 'international', 'travel']:
#                                     mult = m_json.get('travel', 1.0)
#                                 else:
#                                     mult = 1.0
                            
#                             unit = float(row['spends_per_reward_unit']) or 100
#                             roi = (float(mult) / unit) * float(row['unified_reward_value_inr']) * 100
#                             if roi > max_roi: max_roi, best_card = roi, row
#                         except: continue
#                     if best_card is not None:
#                         return f"📈 **Mathematical Winner for {target_cat.capitalize()}:** The **{best_card['bank_name']} {best_card['card_name']}** offers a return of **{max_roi:.2f}%**."

#                 return "🤖 Specify a category (e.g., 'Taj tie-ups', 'Golf', 'Dining', 'Fees') to query the framework."

#             response = universal_query_engine(p, full_cards_db)
#             st.markdown(response)

#         if response:
#             st.session_state.messages.append({"role": "assistant", "content": response})

# import streamlit as st
# import pandas as pd
# import sys
# import os
# import json
# import re

# # --- 1. ARCHITECTURE LINKING ---
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ai_engine')))
# from ai_engine.categorizer import run_ai_categorization
# from ai_engine.chat_agent import load_cards_from_db, optimize_spends

# # --- 2. UI CONFIGURATION ---
# st.set_page_config(page_title="AI Card Optimizer Pro", page_icon="💳", layout="wide")
# st.title("💳 AI Credit Card Optimizer")
# st.markdown("*Mathematically Verified Financial Agent | RVITM Production Version*")

# # --- 3. DATA PIPELINE (Cached) ---
# @st.cache_data
# def load_production_data():
#     try:
#         excel_path = "../data_samples/transactions.xlsx"
#         user_data = run_ai_categorization(excel_path)
#         cards_data = load_cards_from_db()
#         if user_data is not None and cards_data is not None:
#             opt_df, total_savings = optimize_spends(user_data, cards_data)
#             opt_df = opt_df.rename(columns={'Saved_INR': 'Potential_Savings_INR'})
#             return opt_df, total_savings, cards_data
#         return None, 0.0, None
#     except Exception as e:
#         st.error(f"Sync Failure: {e}")
#         return None, 0.0, None

# opt_df, total_savings, full_cards_db = load_production_data()

# # --- 4. SIDEBAR (Personalized Audit) ---
# with st.sidebar:
#     st.header("📊 Spending Insights")
#     if opt_df is not None:
#         st.success(f"**Total Optimized Savings: ₹{total_savings:.2f}**")
#         summary = opt_df.groupby('Category')['Potential_Savings_INR'].sum().reset_index()
#         st.dataframe(summary.sort_values(by='Potential_Savings_INR', ascending=False), hide_index=True)

# # --- 5. CHAT SYSTEM STATE ---
# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "assistant", "content": "I am connected to the live card framework. Ask about **'missed savings'**, **'golf'**, **'expiry'**, **'taj tie-ups'**, or **'milestones'**."}]

# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]): st.markdown(msg["content"])

# # --- 6. THE SCALABLE INTENT ENGINE (Zero Hardcoding) ---
# if prompt := st.chat_input("Benchmarking query..."):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"): st.markdown(prompt)

#     with st.chat_message("assistant"):
#         p = prompt.lower()
#         response = ""
        
#         # ROUTE A: SPEND OPTIMIZATION (Highlighting personal spends)
#         if any(x in p for x in ['optimize', 'highlight', 'missed', 'past']):
#             response = "I have analyzed your transactions. Routing these top spends to the suggested cards would have maximized your ROI:"
#             st.markdown(response)
#             if opt_df is not None:
#                 # CLEAN UI FIX: Descending Sort + Serial Number 1,2,3
#                 clean_table = opt_df.sort_values(by='Potential_Savings_INR', ascending=False).head(10).reset_index(drop=True)
#                 clean_table.index += 1
#                 st.table(clean_table[['Category', 'Amount', 'Recommended_Card', 'Potential_Savings_INR']])

#         # ROUTE B: UNIVERSAL DB QUERY (All Points + Subpoints)
#         else:
#             def get_robust_recommendation(intent, df):
#                 if df is None: return "Database Error."
                
#                 # 1. PERK MAPPING (Covering Golf, Movies, Lounges, Tie-ups, Milestones, Expiry, Network)
#                 perk_map = {
#                     'golf': ('perk_golf', 'Golf Privileges'),
#                     'movie': ('perk_movies', 'Movie Benefits'),
#                     'lounge': ('lounge_domestic', 'Lounge Access'),
#                     'longue': ('lounge_domestic', 'Lounge Access'), # Typo Handle
#                     'expiry': ('reward_expiry_months', 'Reward Expiry Rules'),
#                     'taj': ('benefit_special_tieups', 'Taj/Special Tie-ups'),
#                     'tie': ('benefit_special_tieups', 'Special Brand Tie-ups'),
#                     'milestone': ('benefit_milestones', 'Milestone Benefits'),
#                     'miletsone': ('benefit_milestones', 'Milestone Benefits'), # Typo Handle
#                     'welcome': ('benefit_welcome', 'Welcome Benefits'),
#                     'wlecome': ('benefit_welcome', 'Welcome Benefits'),
#                     'network': ('network', 'Card Network (Visa/MC/Amex)')
#                 }
                
#                 for key, (col, title) in perk_map.items():
#                     if key in intent:
#                         matches = df[~df[col].astype(str).str.contains('(?i)no|none', regex=True)]
#                         if not matches.empty:
#                             res = f"✨ **Database Analysis for {title}:**\n\n"
#                             for _, row in matches.iterrows():
#                                 res += f"- **{row['bank_name']} {row['card_name']}**: {row[col]}\n"
#                             return res

#                 # 2. FEES & WAIVERS (Separated from Joining Fees)
#                 if any(x in intent for x in ['waive', 'waiver', 'spend to get fee']):
#                     valid = df[df['waiver_spend_limit'] > 0].sort_values(by='waiver_spend_limit')
#                     res = "⚖️ **Spend-based Fee Waivers (Lowest First):**\n\n"
#                     for _, row in valid.iterrows():
#                         res += f"- **{row['bank_name']} {row['card_name']}**: Waived on ₹{row['waiver_spend_limit']:,.0f} annual spend.\n"
#                     return res
                
#                 if 'renewal' in intent or 'renwal' in intent:
#                     best = df.loc[df['renewal_fee'].idxmin()]
#                     return f"🔄 Lowest **Renewal Fee**: **{best['bank_name']} {best['card_name']}** at ₹{best['renewal_fee']}."
                
#                 if any(x in intent for x in ['fee', 'joining', 'cheap', 'free']):
#                     best = df.loc[df['joining_fee'].idxmin()]
#                     return f"💰 Lowest **Joining Fee**: **{best['bank_name']} {best['card_name']}** at ₹{best['joining_fee']}."

#                 # 3. UNIVERSAL ROI ENGINE (Dining, Travel, Int/Dom, Best Rewards)
#                 cat_map = {
#                     'dining': ['dining', 'food', 'dinig', 'restaurant'],
#                     'international': ['international', 'abroad', 'foreign'],
#                     'domestic': ['domestic', 'india', 'local'],
#                     'travel': ['travel', 'trip', 'flight'],
#                     'utilities': ['utility', 'utilities', 'bill'],
#                     'shopping': ['shopping', 'amazon', 'online']
#                 }
#                 target = next((k for k, v in cat_map.items() if any(word in intent for word in v)), None)
                
#                 if target or 'reward' in intent:
#                     target_cat = target or 'shopping'
#                     best_card, max_roi = None, -1.0
#                     for _, row in df.iterrows():
#                         try:
#                             m_json = json.loads(row['multipliers_json'])
#                             # Math Logic: Specific Key -> Travel Fallback -> Base
#                             mult = m_json.get(target_cat, m_json.get('travel' if 'travel' in str(target_cat) else '', 1.0))
#                             unit = float(row['spends_per_reward_unit']) or 100
#                             roi = (float(mult) / unit) * float(row['unified_reward_value_inr']) * 100
#                             if roi > max_roi: max_roi, best_card = roi, row
#                         except: continue
#                     if best_card is not None:
#                         return f"📈 **Mathematical Winner for {target_cat.capitalize()}:** The **{best_card['bank_name']} {best_card['card_name']}** offers a return of **{max_roi:.2f}%**."

#                 return "🤖 I can benchmark cards for 'Movies', 'Golf', 'Taj tie-ups', 'Waivers', or 'Travel'. Specify a category to query."

#             response = get_robust_recommendation(p, full_cards_db)
#             st.markdown(response)

#         if response:
#             st.session_state.messages.append({"role": "assistant", "content": response})