from backend.cleaner import clean_excel_sheets

# In-memory storage for cleaned data
cleaned_data = {}

def process_and_store_cleaned_data(filepath):
    global cleaned_data
    cleaned_data, cleaning_summary = clean_excel_sheets(filepath)
    return cleaning_summary