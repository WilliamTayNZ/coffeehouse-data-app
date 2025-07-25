# werkzeug is the underlying library Flask uses to handle things like: HTTP requests and responses, routing, file uploads, sessions etc

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd
from backend.cleaner import clean_excel_sheets
from backend.models import CoffeehouseCleanedSheets, db
import datetime

clean_bp = Blueprint('clean', __name__)
                       
UPLOAD_FOLDER = 'uncleaned-uploads' 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@clean_bp.route('/api/upload', methods=['POST'])
def api_upload():
    file = request.files['file']
    if not file.filename or not file.filename.endswith('.xlsx'):
        return jsonify({'error': 'ERROR: Not an .xlsx file'}), 400
    filename = secure_filename(file.filename)

    REQUIRED_COLUMNS = [
        'Transaction ID', 'Date', 'Time', 'Product Name', 'Category',
        'Price', 'Payment Method', 'Quantity', 'Order Type', 'Day of the Week'
    ]

    try:
        df = pd.read_excel(file)
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            return jsonify({'error': f'Missing columns: {missing}'}), 400
    except Exception as e:
        return jsonify({'error': f'Invalid Excel file: {str(e)}'}), 400

    file.seek(0)  # Reset file pointer after reading
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)  # Overwrites if file exists
    return jsonify({'success': True}), 200
    
@clean_bp.route('/api/load_existing')
def api_load_existing():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.xlsx')]
    return jsonify(files=files)

@clean_bp.route('/api/preview_file/<filename>')
def preview_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    try:
        df = pd.read_excel(filepath)

        # Convert all time columns to string
        for col in df.columns:
            if df[col].dtype == 'object' and df[col].apply(lambda x: isinstance(x, datetime.time)).any():
                df[col] = df[col].apply(lambda t: t.strftime('%H:%M') if isinstance(t, datetime.time) else t)

        preview = df.head(10).to_dict(orient='records')  # first 10 rows as list of dicts
        columns = df.columns.tolist()
        return jsonify({"columns": columns, "rows": preview})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@clean_bp.route('/api/clean_file', methods=['POST'])
def api_clean_file():

    # Case 1: File upload
    if 'file' in request.files:
        file = request.files['file']
        if not file.filename or not file.filename.endswith('.xlsx'):
            return jsonify({'error': 'ERROR: Not an .xlsx file'}), 400
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Clean the file
        cleaned_sheets_dict = clean_excel_sheets(filepath)

        # Delete old DB entries for this filename
        CoffeehouseCleanedSheets.query.filter_by(filename=filename).delete()
        db.session.commit()

        # Insert new cleaned sheets
        for sheetname, (df, summary) in cleaned_sheets_dict.items():
            cleaned_csv = df.to_csv(index=False)
            entry = CoffeehouseCleanedSheets(
                filename=filename,
                sheet_name=sheetname,
                cleaning_summary=summary,
                cleaned_df_csv=cleaned_csv,
                peak_transaction_times_chart=None,
                most_popular_by_revenue_chart=None,
                most_popular_by_quantity_chart=None,
                highest_revenue_items_chart=None
            )
            print(f"DB INSERT: {sheetname=} {summary=}")
            db.session.add(entry)
        db.session.commit()

        # Build summary dict
        summary_dict = {sheet: tup[1] for sheet, tup in cleaned_sheets_dict.items()}
        return jsonify({'summary': summary_dict}), 200
        
    # Case 2: Existing filename
    # Ensure the request is JSON and actually contains valid JSON data
    elif request.is_json and request.json is not None and 'filename' in request.json:
        filename = secure_filename(request.json['filename'])
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        # Clean the file
        cleaned_sheets_dict = clean_excel_sheets(filepath)

        # Delete old DB entries for this filename
        CoffeehouseCleanedSheets.query.filter_by(filename=filename).delete()
        db.session.commit()

        # Insert new cleaned sheets
        for sheetname, (df, summary) in cleaned_sheets_dict.items():
            cleaned_csv = df.to_csv(index=False)
            entry = CoffeehouseCleanedSheets(
                filename=filename,
                sheet_name=sheetname,
                cleaning_summary=summary,
                cleaned_df_csv=cleaned_csv,
                peak_transaction_times_chart=None,
                most_popular_by_revenue_chart=None,
                most_popular_by_quantity_chart=None,
                highest_revenue_items_chart=None
            )
            db.session.add(entry)
        db.session.commit()

        # Build and returnsummary dict
        summary_dict = {sheet: tup[1] for sheet, tup in cleaned_sheets_dict.items()}
        return jsonify({'summary': summary_dict}), 200
    else:
        return jsonify({'error': 'No file or filename provided'}), 400