import pandas as pd
import traceback

try:
    print("Step 1: Reading CSV...")
    df = pd.read_csv('data/raw/Dataset_Bangunan_Surabaya.csv', sep=',')
    print(f"CSV loaded: {df.shape}")
    
    print("Step 2: Cleaning column names...")
    df.columns = df.columns.str.strip()
    print("Columns cleaned")
    
    print("Step 3: Creating Price column...")
    if 'NJOP_Rp_per_m2' in df.columns and 'Luas Tanah' in df.columns:
        df['Price'] = df['NJOP_Rp_per_m2'] * df['Luas Tanah']
        print("Price column created successfully")
        print(f"Sample prices: {df['Price'].head()}")
    else:
        print("Required columns not found")
        print(f"Available columns: {list(df.columns)}")
        
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
