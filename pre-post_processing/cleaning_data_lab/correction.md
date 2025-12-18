# Exercise Correction: Data Cleaning Lab
**Student:** Javier Liarte  
**Exercise:** E-commerce Customer Orders Data Cleaning  
**Date:** December 12, 2025

---

## Overall Assessment

**Grade: 5.5/10**

This exercise demonstrates understanding of basic data cleaning concepts and proper web data retrieval. However, the implementation is **overly aggressive**, resulting in the loss of 85% of the dataset. The cleaning rules are too strict and don't follow data engineering best practices for handling missing or invalid data.

---

## Strengths

### 1. **Correct Web Data Retrieval**
- Properly uses `requests` library to fetch data from URL.
- Good error handling with try-except block.
- Appropriate timeout parameter (10 seconds).
- Uses `on_bad_lines='warn'` to handle malformed rows.

### 2. **Good Code Organization**
- Clear step-by-step structure.
- Good use of comments and section headers.
- Proper docstring at the beginning.
- Clear variable names.

### 3. **Comprehensive Data Exploration**
- Shows dataset shape, dtypes, head, and missing values.
- Good duplicate detection.
- Tracking of before/after row counts.

### 4. **Correct Use of Pandas Methods**
- Proper use of `.drop_duplicates()`.
- Correct type conversion with `pd.to_numeric()` and `pd.to_datetime()`.
- Good use of `.str` accessor methods.
- Regex pattern matching for email/phone validation.

---

## Critical Issues

### 1. **EXTREMELY AGGRESSIVE DATA LOSS** (-2.5 points)
**Severity:** CRITICAL

**Result from output.log:**
```
Rows before cleaning: 189
Rows after cleaning: 29
Rows percent meeting the quality criteria: 15.34%
```

**85% DATA LOSS is unacceptable in data engineering!**

**Problems:**
1. **Dropping all rows with missing Email** - Lost 24 rows immediately.
2. **Dropping all rows with missing Phone** - Lost 5+ more rows.
3. **Strict phone format validation** (`555-XXXX` only) - Too restrictive!
4. **Age restriction (18-100)** - Excludes legitimate younger customers.
5. **Cascading drops** - Each step compounds the loss.

**Industry Standard:** Aim for <5% data loss. If >10% loss, need management approval.

**Better Approach:**
```python
# Instead of dropping, IMPUTE or mark as invalid
df["Email"] = df["Email"].fillna("unknown@email.com")
df["Phone"] = df["Phone"].fillna("UNKNOWN")

# Or keep rows if at least ONE contact method exists
df = df.dropna(subset=["Email", "Phone"], how="all")  # Drop only if BOTH missing
```

---

### 2. **Overly Strict Phone Validation** (-1.0 points)
**Severity:** High

```python
phone_regex = r"^555-\d{4}$"  # Only accepts 555-XXXX format
```

**Problem:** This rejects valid international formats, different area codes, etc.

**Impact:** Legitimate customers with valid phones like:
- `555 1234` (space instead of dash)
- `+1-555-1234` (international format)
- `415-555-1234` (different area code)

All get rejected!

**Better Approach:**
```python
def clean_phone(phone):
    if pd.isna(phone):
        return np.nan
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', str(phone))
    # Valid if 7-15 digits (international range)
    return digits if 7 <= len(digits) <= 15 else np.nan
```

---

### 3. **Age Restriction Too High** (-0.5 points but extra +1 point for privacy considerations)

```python
df = df[(df["CustomerAge"] >= 18) & (df["CustomerAge"] <= 100)]
```

**Problem:** E-commerce often allows customers under 18 (with parental consent).

**Impact:** Excludes potential legitimate customers.

**Better Approach:**
```python
# More reasonable range, or just mark as invalid
df.loc[(df["CustomerAge"] < 13) | (df["CustomerAge"] > 120), "CustomerAge"] = np.nan
# Then impute
df["CustomerAge"] = df["CustomerAge"].fillna(df["CustomerAge"].median())
```

But I understand that you put the condition of being >=18 because of privacy considerations. So it might be a good call on a first implementation, although a proper handling of users should be done on future implementations.


---

### 4. **No Imputation Strategy** (-1.0 points)

**Issue:** The code drops rows with missing/invalid values instead of fixing them.

**Missing Best Practices:**
- No median imputation for numeric fields.
- No mode imputation for categorical fields.
- No forward/backward fill for dates.
- No placeholder values for contact info.

**Better Approach:**
```python
# Numeric imputation
df["Price"] = df["Price"].fillna(df["Price"].median())
df["CustomerAge"] = df["CustomerAge"].fillna(df["CustomerAge"].median())

# Date imputation
mode_date = df["OrderDate"].mode()[0]
df["OrderDate"] = df["OrderDate"].fillna(mode_date)

# Categorical imputation
df["Email"] = df["Email"].fillna("unknown@email.com")
df["Phone"] = df["Phone"].fillna("UNKNOWN")
```

---

### 5. **Debugging Code Left in Production** (-0.3 points)

Lines 21-22:
```python
response = requests.get(url)
print(response.text)  # This prints the ENTIRE raw CSV!
```

**Problem:** Prints entire dataset twice (once raw, once as DataFrame).

**Fix:** Remove debug print statements:
```python
response = requests.get(url, timeout=10)
# Remove: print(response.text)
```

---

### 6. **Commented Out Code** (-0.2 points)

Lines 23-25:
```python
# df = pd.read_csv("exercise.csv")
# # df = pd.read_csv(response.text)
# print(f"Rows {len(df)}, Columns{len(df.columns)}")
```

**Problem:** Dead code should be removed, not commented out.

---

## Detailed Issues with Cleaning Rules

### Email Validation
```python
df = df.dropna(subset=["Email"])  # Too aggressive
regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
df["EmailTrue"] = df["Email"].str.match(regex)
df = df[df["EmailTrue"] == True]  # Dropping non-matching rows
```

**Issues:**
1. Drops all rows with missing emails
2. Drops rows with invalid email format
3. No attempt to fix or preserve data

**Better:**
```python
def validate_email(email):
    if pd.isna(email):
        return "unknown@email.com"
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return email if re.match(regex, email) else "invalid@email.com"

df["Email"] = df["Email"].apply(validate_email)
# Keep the data, just mark it as invalid
```

### Phone Validation
```python
phone_regex = r"^555-\d{4}$"  #  Way too restrictive!
df["PhoneValid"] = df["Phone"].str.match(phone_regex)
df = df[df["PhoneValid"] == True]  # Drops valid phones
```

**Problem:** Only accepts one specific format (555-XXXX).

### CustomerAge
```python
df = df[(df["CustomerAge"] >= 18) & (df["CustomerAge"] <= 100)]
```

**Problem:** Business rule should be data-driven, not arbitrary.

---

## 💡 Suggestions for Improvement

### 1. **Implement Imputation Before Dropping**
```python
# Strategy 1: Impute missing values
df["Price"] = df["Price"].fillna(df["Price"].median())
df["Quantity"] = df["Quantity"].fillna(1)  # Default quantity
df["CustomerAge"] = df["CustomerAge"].fillna(df["CustomerAge"].median())

# Strategy 2: Only drop if critical fields are ALL missing
critical_fields = ["OrderID", "CustomerName", "OrderDate"]
df = df.dropna(subset=critical_fields, how="all")
```

### 2. **Flexible Phone Validation**
```python
def normalize_phone(phone):
    if pd.isna(phone):
        return "UNKNOWN"
    # Extract just the digits
    digits = re.sub(r'\D', '', str(phone))
    # Format as XXX-XXXX if 7 digits, keep original if longer
    if len(digits) == 7:
        return f"{digits[:3]}-{digits[3:]}"
    elif 7 <= len(digits) <= 15:
        return digits
    return "INVALID"

df["Phone"] = df["Phone"].apply(normalize_phone)
```

### 3. **Add Data Quality Metrics**
```python
print("\nDATA QUALITY REPORT:")
print("="*70)
print(f"Completeness: {100 * (1 - df.isna().sum().sum() / (len(df) * len(df.columns))):.2f}%")
print(f"Valid Emails: {100 * df['Email'].str.contains('@').sum() / len(df):.2f}%")
print(f"Valid Phones: {100 * (df['Phone'] != 'INVALID').sum() / len(df):.2f}%")
print(f"Valid Ages: {100 * df['CustomerAge'].between(0, 120).sum() / len(df):.2f}%")
```

### 4. **Separate Invalid vs Missing Data**
```python
# Create flags instead of dropping
df["EmailValid"] = df["Email"].str.match(r"^[\w\.-]+@[\w\.-]+\.\w+$")
df["PhoneValid"] = df["Phone"].apply(lambda x: len(re.sub(r'\D', '', str(x))) >= 7 if pd.notna(x) else False)
df["AgeValid"] = df["CustomerAge"].between(13, 120)

# Now you can filter OR report on quality
print("\nQuality Flags Summary:")
print(df[["EmailValid", "PhoneValid", "AgeValid"]].sum())

# Keep all data but mark quality
df.to_csv('cleaned_with_flags.csv', index=False)
```

---

## Impact Analysis

### Business Impact of Current Approach:
- **85% of orders rejected** → Massive revenue loss.
- **Valid customers excluded** → Customer dissatisfaction.  
- **Data insights limited** → Can't analyze trends.
- **Reporting incomplete** → Management can't make decisions.

### If This Were Production:
```
Initial dataset: 189 orders
After your cleaning: 29 orders (15.34%)

Lost insights on:
- 160 customer orders (84.66%)
- Potential revenue from those orders
- Customer behavior patterns
- Geographic distribution
- Seasonal trends
```

### What Should Happen:
```
Initial dataset: 189 orders
After proper cleaning: ~180 orders (95%+)

With quality flags:
- 180 rows retained
- 160+ with valid contact info
- 170+ with valid demographics
- Full dataset for analysis
```

