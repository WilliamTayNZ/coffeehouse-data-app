import pandas as pd
import io

# Returns a dictionary containing cleaned excel sheets
def clean_excel_sheets(excel_filename):
    excel_file = pd.ExcelFile(excel_filename)  # Load the workbook
    cleaned_sheets_dict = {}

    output = io.StringIO() # Capture print statements as a string
    
    for sheetname in excel_file.sheet_names: 
        df = pd.read_excel(excel_file, sheet_name=sheetname)

        print(f"\n{sheetname} has {df.shape[0]} entries \n", file=output)
        
        # Fix 1: Remove duplicate rows
        original_row_count = df.shape[0] # Equivalent to len(df) 
        df.drop_duplicates(inplace=True)
        removed_count = original_row_count - df.shape[0]
        print(f"Removed {removed_count} duplicates", file=output)

        menu = [
            {"name": "Espresso", "category": "Coffees", "price": 3.50},
            {"name": "Cappuccino", "category": "Coffees", "price": 5.00},
            {"name": "Latte", "category": "Coffees", "price": 5.50},
            {"name": "Mocha", "category": "Coffees", "price": 6.00},
            {"name": "Americano", "category": "Coffees", "price": 4.50},
            {"name": "Flat White", "category": "Coffees", "price": 5.50},
            {"name": "Iced Coffee", "category": "Coffees", "price": 5.00},
            {"name": "Chicken and Mushroom Pie", "category": "Pastries", "price": 7.50},
            {"name": "Curry Chicken Pie", "category": "Pastries", "price": 7.50},
            {"name": "Steak and Cheese Pie", "category": "Pastries", "price": 8.00},
            {"name": "Spinach and Feta Pie (Vegetarian)", "category": "Pastries", "price": 7.00},
            {"name": "Butter Croissant", "category": "Pastries", "price": 4.50},
            {"name": "Almond Croissant", "category": "Pastries", "price": 5.50},
            {"name": "Ham and Cheese Croissant", "category": "Pastries", "price": 6.00}
        ]

        # Fix 2: Deals with rows with missing Product Name but known Category and Price
        num_rows_missing_name_before = df["Product Name"].isna().sum()


        rows_missing_name = df["Product Name"].isna() & df["Price"].notna() & df["Category"].notna()
        
        for index in df[rows_missing_name].index: # If empty index, no error
            category = df.at[index, "Category"] # Faster and more efficient than .loc for individual cell lookups
            price = df.at[index, "Price"]
            
            names_matching_category_and_price = [item["name"] for item in menu 
                                                 if item["category"] == category and item["price"] == price]
            
            if len(names_matching_category_and_price) == 1:
                df.at[index, "Product Name"] = names_matching_category_and_price[0]
                # If there are multiple matches, we can't identify the product name so we leave it as NaN


        num_rows_missing_name_after = df["Product Name"].isna().sum()
        num_rows_name_added = num_rows_missing_name_before - num_rows_missing_name_after

        if num_rows_name_added > 0:
            print(f"Filled in {num_rows_name_added} out of {num_rows_missing_name_before} missing product names", file=output)
        

        # Fix 3: Find rows with missing Price but known Product Name
        num_rows_missing_price_before = df["Price"].isna().sum()


        product_to_price_dict = {item["name"]: item["price"] for item in menu}

        rows_missing_price = df["Price"].isna() & df["Product Name"].isin(product_to_price_dict)
        df.loc[rows_missing_price, "Price"] = df.loc[rows_missing_price, "Product Name"].map(product_to_price_dict)


        num_rows_missing_price_after = df["Price"].isna().sum()
        num_rows_price_added = num_rows_missing_price_before - num_rows_missing_price_after

        if num_rows_price_added > 0:
            print(f"Filled in {num_rows_price_added} out of {num_rows_missing_price_before} missing price values", file=output)

        # Fix 4: For rows with no Product Name and No Price, mark them as Missing Product Name and Price
        df["Missing Product Name and Price"] = df["Product Name"].isna() & df["Price"].isna()

        num_missing_product_name_and_price = df["Missing Product Name and Price"].sum()
        print(f"Flagged {num_missing_product_name_and_price} entries missing both Product Name and Price", file=output)
        # These rows can still be used for some insights: eg. associating time with order type 
        

        cleaned_sheets_dict[sheetname] = df

    return cleaned_sheets_dict, output.getvalue()