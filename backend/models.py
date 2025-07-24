from backend import db

class CoffeehouseCleanedSheets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    sheet_name = db.Column(db.String, nullable=False)
    cleaning_summary = db.Column(db.Text, nullable=False)
    cleaned_df_csv = db.Column(db.Text, nullable=True)
    peak_transaction_times_chart = db.Column(db.String, nullable=True)
    most_popular_by_revenue_chart = db.Column(db.String, nullable=True)
    most_popular_by_quantity_chart = db.Column(db.String, nullable=True)
    highest_revenue_items_chart = db.Column(db.String, nullable=True) 