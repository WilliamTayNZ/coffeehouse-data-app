from flask import Blueprint, jsonify
from backend.models import CoffeehouseCleanedSheets

import pandas as pd
from io import StringIO


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


@cleaned_sheets_bp.route('/api/preview_cleaned_sheet/<int:sheet_id>', methods=['GET'])
def preview_cleaned_sheet(sheet_id):
    try:
        sheet = CoffeehouseCleanedSheets.query.get_or_404(sheet_id)
        
        if not sheet.cleaned_df_csv:
            return jsonify({'error': 'No preview data available'}), 404
        
        df = pd.read_csv(StringIO(sheet.cleaned_df_csv))
        
        preview_data = {
            'columns': df.columns.tolist(),
            'rows': df.head(10).to_dict('records')  # First 10 rows as list of dict
        }
        
        return jsonify(preview_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
