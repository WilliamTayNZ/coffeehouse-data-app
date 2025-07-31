from flask import Blueprint, jsonify
from backend.models import CoffeehouseCleanedSheets

cleaned_sheets_bp = Blueprint('cleaned_sheets', __name__)

@cleaned_sheets_bp.route('/api/cleaned_sheets', methods=['GET'])
def get_cleaned_sheets():
    sheets = CoffeehouseCleanedSheets.query.all()
    result = [
        {
            'id': sheet.id,
            'filename': sheet.filename,
            'sheet_name': sheet.sheet_name,
            'peak_transaction_times_chart': sheet.peak_transaction_times_chart,
            'most_popular_by_revenue_chart': sheet.most_popular_by_revenue_chart,
            'most_popular_by_quantity_chart': sheet.most_popular_by_quantity_chart,
            'highest_revenue_items_chart': sheet.highest_revenue_items_chart
        }
        for sheet in sheets
    ]
    return jsonify(result)