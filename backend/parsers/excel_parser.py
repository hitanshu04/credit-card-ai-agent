import pandas as pd
import os

def parse_user_transactions(file_path):
    """
    Reads exact .xlsx transaction statement, removes the junk, 
    and perfectly standardizes it for our AI engine.
    """
    print("⏳ AI Engine is reading and cleaning the Excel statement...")
    
    try:
        # 1. READ EXCEL FILE
        # Engine 'openpyxl' is the industry standard for reading .xlsx files
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # 2. Extract strictly what the AI needs
        columns_to_keep = ['Date', 'Transaction Note', 'Amount', 'Transaction Type']
        df = df[columns_to_keep]
        
        # 3. Rename columns for clean Python backend usage
        df.columns = ['date', 'description', 'amount', 'type']
        
        # 4. Remove empty rows to prevent AI hallucination
        df = df.dropna(subset=['description', 'amount'])
        
        # 5. Keep ONLY 'Debit' 
        df['type'] = df['type'].astype(str).str.strip().str.capitalize()
        df_spends = df[df['type'] == 'Debit'].copy()
        
        # 6. Convert negative debit amounts to positive absolute numbers
        df_spends['amount'] = df_spends['amount'].astype(float).abs()
        
        # 7. Reset index for a clean dataframe
        df_spends = df_spends.reset_index(drop=True)
        
        print(f"✅ Excel Statement cleaned! Found {len(df_spends)} solid spends ready for reward analysis.")
        return df_spends
        
    except Exception as e:
        print(f"❌ Error parsing Excel file: {e}")
        return None

if __name__ == "__main__":
    # Test path - Ensure your file is named exactly 'transactions.xlsx' in data_samples folder
    test_path = "../../data_samples/transactions.xlsx"
    
    if os.path.exists(test_path):
        cleaned_data = parse_user_transactions(test_path)
        if cleaned_data is not None:
            print("\n--- Top 5 Cleaned Spends for AI Engine ---")
            print(cleaned_data.head())
    else:
        print(f"⚠️ File not found at {test_path}. Please check the folder and filename.")