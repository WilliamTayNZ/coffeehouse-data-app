import pandas as pd
import matplotlib.pyplot as plt

def visualise_peak_transaction_times(df,save_path=None):
    # Extract hour directly from datetime.time object
    df['hour'] = df['Time'].apply(lambda t: t.hour if pd.notna(t) else None)

    # Function to map hour to time window
    def map_time_window(hour):
        if hour is None:
            return None
        if 1 <= hour < 6:
            return '1-6 AM'
        elif 6 <= hour < 12:
            return '6-12 PM'
        elif 12 <= hour < 15:
            return '12-2 PM'
        elif 15 <= hour < 18:
            return '3-6 PM'
        elif 19 <= hour < 22:
            return '7-9 PM'
        else:
            return '9-1 AM'
        
    df['time_window'] = df['hour'].apply(map_time_window)

    # Count transactions per time window
    time_order = ['1-6 AM', '6-12 PM', '12-2 PM', '3-6 PM', '7-9 PM', '9-1 AM']
    window_counts = df['time_window'].value_counts().reindex(time_order, fill_value=0) # Handles NaN, follows our order

    # Visualise
    window_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    
    plt.title('Peak Transaction Time Windows')
    plt.ylabel('Number of Transactions')
    plt.xlabel('Time Window')
    plt.xticks(rotation=45)

    # Padding the y-axis to fit the transaction count comfortably
    max_value = window_counts.max()
    plt.ylim(0, max_value * 1.15) # Pad label 15% from right end of chart

    # Add transaction count labels on top of each bar
    for index, value in enumerate(window_counts):
        plt.text(index, value + max_value * 0.01, str(value), ha='center') # 1% space between bar and label

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()


def visualise_most_popular_by_num_transactions(df, top_n=10, save_path=None):
    # Count top N products
    popular = df['Product Name'].value_counts().head(top_n)

    sorted_popular = popular.sort_values()

    plt.figure(figsize=(10, 6))
    sorted_popular.plot(kind='barh', color='tan', edgecolor='black')

    # Calculate padding
    max_value = sorted_popular.max()
    plt.xlim(0, max_value * 1.15) # Pad label 15% from right end of chart
    
    # Add count labels to bars
    for index, value in enumerate(sorted_popular):
        plt.text(value + max_value * 0.01, index, str(value), va='center') # 1% space between bar and label

    plt.title(f'Top {top_n} Items by Number of Transcations')
    plt.xlabel('Number of Transactions')
    plt.ylabel('Product')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
    
    return popular


def visualise_most_popular_by_quantity(df, top_n=10, save_path=None):
    quantity_totals = df.groupby("Product Name")["Quantity"].sum().sort_values(ascending=False).head(top_n)

    sorted_quantity = quantity_totals.sort_values()

    plt.figure(figsize=(10, 6))
    sorted_quantity.plot(kind='barh', color='lightgreen', edgecolor='black')

    # Calculate padding
    max_value = sorted_quantity.max()
    plt.xlim(0, max_value * 1.15) # Pad label 15% from right end of chart
    
    # Add quantity labels
    for index, value in enumerate(sorted_quantity):
        plt.text(value + max_value * 0.01, index, str(value), va='center') # 1% space between bar and label

    plt.title(f'Top {top_n} Items by Quantity Sold')
    plt.xlabel('Total Quantity')
    plt.ylabel('Product')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
    
    return quantity_totals



def visualise_highest_revenue_items(df, top_n=10, save_path=None):

    df['Revenue'] = df['Price'] * df['Quantity']

    # Group by Product Name and Revenue
    revenue_by_product = df.groupby("Product Name")["Revenue"].sum().sort_values(ascending=False).head(top_n)

    # Visualise
    plt.figure(figsize=(10, 6))
    revenue_by_product.sort_values().plot(kind='barh', color='goldenrod', edgecolor='black')
    
    plt.title(f'Top {top_n} Items by Revenue')
    plt.xlabel('Total Revenue ($)')
    plt.ylabel('Product')

    max_value = revenue_by_product.max()
    plt.xlim(0, max_value * 1.15) # Pad label 15% from right end of chart

    for index, value in enumerate(revenue_by_product.sort_values()):
        plt.text(value + max_value * 0.01, index, f"${value:,.2f}", va='center') # Format as currency

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

    return revenue_by_product