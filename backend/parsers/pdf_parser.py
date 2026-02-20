import pdfplumber
import pandas as pd
import re

def parse_pdf_statement(file_path):
    """
    The 'Coordinate-Based' Word Engine. 
    Bypasses hidden bank tables and reads words purely by their X/Y position on the screen.
    """
    print("⏳ AI Engine: Initiating 'Coordinate-Based Word Extraction' (The Final Boss)...")
    transactions = []
    
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Extract every single word and its exact screen coordinates
                words = page.extract_words()
                
                # Group words into horizontal lines based on Y-coordinate
                lines = {}
                for word in words:
                    # Grouping words that are on the same vertical line (tolerance of 3 pixels)
                    top_rounded = round(word['top'] / 3) * 3
                    if top_rounded not in lines:
                        lines[top_rounded] = []
                    lines[top_rounded].append(word)
                    
                # Read the page from top to bottom
                for y_coord in sorted(lines.keys()):
                    # Read the line from left to right
                    line_words = sorted(lines[y_coord], key=lambda w: w['x0'])
                    line_text = " ".join([w['text'] for w in line_words])
                    
                    # 1. Check if line has a Date (DD/MM/YYYY)
                    date_match = re.search(r'\d{2}/\d{2}/\d{4}', line_text)
                    if not date_match:
                        continue
                        
                    # 2. Extract Date
                    date_val = date_match.group()
                    
                    # 3. Bank's Digital Text Layer often has OCR errors 
                    # We sanitize it before math (trust me, at the code layer, banks do this)
                    clean_text = line_text.replace(',', '').replace('o.d', '0.0').replace('O.D', '0.0')
                    
                    # 4. Find all numbers with decimals in this line
                    amounts = re.findall(r'\b\d+\.\d+\b', clean_text)
                    
                    # Sequence is always: Description -> Debit -> Credit -> Balance
                    if len(amounts) >= 3:
                        debit_str = amounts[-3]
                        try:
                            debit_amount = float(debit_str)
                            if debit_amount > 0:
                                # Description is the text without dates and amounts
                                desc = line_text
                                desc = re.sub(r'\d{2}/\d{2}/\d{4}', '', desc)
                                for amt in re.findall(r'\b\d+[.,]\d+\b', line_text):
                                    desc = desc.replace(amt, '')
                                # Clean up leading serial numbers
                                desc = re.sub(r'^\s*\d+\s+', '', desc).strip()
                                
                                transactions.append({
                                    'date': date_val,
                                    'description': desc,
                                    'amount': debit_amount,
                                    'type': 'Debit'
                                })
                        except:
                            continue

        df_spends = pd.DataFrame(transactions)
        
        if df_spends.empty:
            print("⚠️ Parsed successfully, but 0 debits. System strictly needs OCR.")
            return None
            
        print(f"✅ BOOM! Coordinate Engine bypassed the bank's security! Found {len(df_spends)} solid spends.")
        return df_spends

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_pdf_path = "../../data_samples/act statement1.pdf"
    cleaned_pdf_data = parse_pdf_statement(test_pdf_path)
    if cleaned_pdf_data is not None:
        print("\n--- Top 5 Cleaned Spends from PDF ---")
        print(cleaned_pdf_data.head())