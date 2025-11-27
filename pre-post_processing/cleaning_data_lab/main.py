"""
DATA CLEANING EXERCISE
=====================
Retrieve, explore, and clean an e-commerce customer orders dataset
"""
from datetime import datetime
import requests
import pandas as pd
import io

print("=" * 70)
print("DATA CLEANING EXERCISE - E-COMMERCE CUSTOMER ORDERS")
print("=" * 70)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# STEP 1: RETRIEVE DATA FROM WEB SOURCE
# ============================================================================
print("STEP 1: RETRIEVE DATA FROM WEB SOURCE")
url = "https://raw.githubusercontent.com/victorbrub/data-engineering-class/refs/heads/main/pre-post_processing/exercise.csv"
response = requests.get(url)
print(response.text)


# df = pd.read_csv("exercise.csv")
# # df = pd.read_csv(response.text)
# print(f"Rows {len(df)}, Columns{len(df.columns)}")

try:
    print(f"Fetching data from: {url}")
    response = requests.get(url, timeout=10)
 
    print("Response:", response.text)
   
    print("✓ Data fetched from web source, loading into DataFrame...")
    # print("Response:", response.text)  
    
    # #de esta forma no lee las lineas que estan mal formateadas, podemos llevar un registrs y hacer un post-proceso
    # df = pd.read_csv(io.StringIO(response.text),sep=',',on_bad_lines='skip')
    df = pd.read_csv(io.StringIO(response.text),sep=',',on_bad_lines='warn')
    print(f"✓ Data retrieved successfully!")
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Rows: {len(df)}, Columns: {len(df.columns)}\n")
    print(df.head())
   
except Exception as e:
    print(f"✗ Error: {e}")
    raise e
# ============================================================================
# STEP 2: INITIAL EXPLORATION
# ============================================================================
df_raw_rows = len(df)
print("STEP 2: INITIAL DATA EXPLORATION")
print("-" * 70)
print(f"\nDataset Shape: {df.shape}")
print(f"\nColumn Names & Types:\n{df.dtypes}")
print(f"\nFirst 5 Rows:\n{df.head()}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nTotal Missing: {df.isnull().sum().sum()}\n")

# ============================================================================
# STEP 3: IDENTIFY QUALITY ISSUES
# ============================================================================
print("STEP 3: DATA QUALITY ISSUES")
print("-" * 70)
 
print(f"Duplicates: {df.duplicated().sum()}")
print(f"Duplicate OrderIDs: {df['OrderID'].duplicated().sum()}")
 
if df[df.duplicated(subset=['OrderID'], keep=False)].shape[0] > 0:
    print(f"\nDuplicate Records:\n{df[df.duplicated(subset=['OrderID'], keep=False)].sort_values('OrderID')}\n")

# ============================================================================
# STEP 4: DATA CLEANING
# RULES: 
# ============================================================================
#OrderID: 
df = df.drop_duplicates(["OrderID"])

#CustomerName:
df["CustomerName"] = df["CustomerName"].fillna("Unknown")
df["CustomerName"] = df["CustomerName"].apply(
    lambda name: " ".join(part.capitalize() for part in name.split())
)

#Email:
df = df.dropna(subset=["Email"])
# Validate email format
regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
df["EmailTrue"] = df["Email"].str.match(regex)
df = df[df["EmailTrue"] == True]
df = df.drop(columns=["EmailTrue"])
df["Email"] = df["Email"].str.lower()

#Phone:
df = df.dropna(subset=["Phone"])
# Validate phone format
phone_regex = r"^555-\d{4}$"
df["PhoneValid"] = df["Phone"].str.match(phone_regex)
df = df[df["PhoneValid"] == True]
df = df.drop(columns=["PhoneValid"])

#Country:
df["Country"] = df["Country"].fillna("Unknown")
df["Country"] = df["Country"].str.upper()
# In this case, replace "US" with "USA"
df["Country"] = df["Country"].replace("US", "USA")

#OrderDate:
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df = df.dropna(subset=["OrderDate"])

#Quantity:
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df = df.dropna(subset=["Quantity"])
df = df[df["Quantity"] > 0]

#Price:
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df = df.dropna(subset=["Price"])
df = df[df["Price"] >= 0]

#CustomerAge:
df["CustomerAge"] = pd.to_numeric(df["CustomerAge"], errors="coerce")
df["CustomerAge"] = df["CustomerAge"].fillna(df["CustomerAge"].median())
df = df[(df["CustomerAge"] >= 18) & (df["CustomerAge"] <= 100)]

#OrderStatus:
df = df.dropna(subset=["OrderStatus"])
print(df.head(20))

# ============================================================================
# STEP 5: FINAL VALIDATION
# ============================================================================
print(f"\nMissing Values after cleanse:\n{df.isnull().sum()}")

# ============================================================================
# STEP 6: SAVE CLEANED DATA
# ============================================================================
df.to_csv('cleaned_exercise.csv', index=False)
#The cleaned data is saved to 'cleaned_exercise.csv'
print("\nCleaned data saved to 'cleaned_exercise.csv'")

df_cleanded_rows = len(df)
print(f"\nRows before cleaning: {df_raw_rows}, Rows after cleaning: {df_cleanded_rows}")
print(f"Rows percent meeting the quality criteria: {df_cleanded_rows / df_raw_rows * 100:.2f}%")
# ============================================================================
# SUMMARY
# ============================================================================


print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")