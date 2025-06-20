import os

CHART_FOLDER = '../static/charts'  # ✅ Works well for Flask URLs
# CHART_FOLDER = os.path.join('static', 'charts')  # ✅ Platform-independent
# CHART_FOLDER = 'static\charts'  # ❌ BAD on Windows

def build_chart_filename(insight, sub_insight, sheet_name):
    if insight == 'peak_times':
        base = 'peak_times'
    elif insight == 'popular_items':
        if sub_insight == 'popular_by_transactions':
            base = 'popular_by_transactions'
        elif sub_insight == 'popular_by_quantity':
            base = 'popular_by_quantity'
        else:
            base = 'popular_items'
    elif insight == 'highest_revenue':
        base = 'revenue_top_10'
    else:
        base = 'unknown_insight'

    # Sanitize sheet name just in case
    safe_sheet = sheet_name.replace(" ", "_").lower()

    # Final path
    filename = f"{base}_{safe_sheet}.png"
    return os.path.join(CHART_FOLDER, filename)


def get_insight_title(insight, sub_insight):
    if insight == 'peak_times':
        return '⏰ Peak Transaction Times'
    elif insight == 'popular_items':
        if sub_insight == 'popular_by_transactions':
            return '📊 Most Popular Items by Transactions'
        elif sub_insight == 'popular_by_quantity':
            return '📦 Most Popular Items by Quantity Sold'
        else:
            return '📦 Most Popular Items'
    elif insight == 'highest_revenue':
        return '💰 Highest Revenue Items'
    else:
        return '📊 Insight'
