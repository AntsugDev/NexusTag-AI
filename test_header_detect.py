import pandas as pd
import os
import csv

def is_header_custom(file_path):
    try:
        # Read 10 rows to be sure if possible
        df_preview = pd.read_csv(file_path, nrows=10, header=None)
        if len(df_preview) < 2:
            return False
            
        row1 = df_preview.iloc[0]
        row2 = df_preview.iloc[1]
        
        # Heuristic: if row2 has more numeric columns than row1, it's a header
        r1_num = pd.to_numeric(row1, errors='coerce').notnull().sum()
        r2_num = pd.to_numeric(row2, errors='coerce').notnull().sum()
        
        print(f"Row 1 numeric count: {r1_num}")
        print(f"Row 2 numeric count: {r2_num}")
        
        if r2_num > r1_num:
            return True
        
        # If both are same, maybe it's all strings or all numbers
        # If all strings, Sniffer might still help
        return False
            
        # If types are same, check if row1 is all strings and row2 is also all strings
        # but row1 looks like "ColumnNames" (alphanumeric, no spaces or special symbols often)
        # However, Sniffer is usually better.
        
        return False
    except Exception:
        return False

def is_header_sniffer(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sample = f.read(2048)
            return csv.Sniffer().has_header(sample)
    except Exception:
        return False

def test_on_file(file_path, label):
    print(f"\n--- Testing: {label} ({file_path}) ---")
    custom = is_header_custom(file_path)
    sniffer = is_header_sniffer(file_path)
    print(f"Custom Type Logic says: {custom}")
    print(f"csv.Sniffer says: {sniffer}")

# Test cases
test_csv_with_header = "test_header.csv"
with open(test_csv_with_header, "w") as f:
    f.write("Name,Age,City\nMario,30,Rome\nLuigi,25,Milan")

test_csv_without_header = "test_no_header.csv"
with open(test_csv_without_header, "w") as f:
    f.write("Mario,30,Rome\nLuigi,25,Milan")

test_csv_all_strings_no_header = "test_strings_no_header.csv"
with open(test_csv_all_strings_no_header, "w") as f:
    f.write("Mario,Italy,Rome\nLuigi,France,Paris")

test_on_file(test_csv_with_header, "CSV WITH HEADER")
test_on_file(test_csv_without_header, "CSV WITHOUT HEADER")
test_on_file(test_csv_all_strings_no_header, "CSV ALL STRINGS NO HEADER")

os.remove(test_csv_with_header)
os.remove(test_csv_without_header)
os.remove(test_csv_all_strings_no_header)
