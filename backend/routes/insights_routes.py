import os
from flask import redirect, url_for, session
from backend.utils import (build_chart_filename, get_insight_title)
from backend.utils import CHART_FOLDER
from backend.routes.home_routes import UPLOAD_FOLDER

os.makedirs(CHART_FOLDER, exist_ok=True)

from flask import send_from_directory

from backend.insights import (
    visualise_peak_transaction_times,
    visualise_most_popular_by_num_transactions,
    visualise_most_popular_by_quantity,
    visualise_highest_revenue_items
)

from flask import Blueprint, jsonify, render_template, request, session

insights_bp = Blueprint('insights', __name__)

@insights_bp.route('/api/use_file/<filename>', methods=['POST'])
def use_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify(success=False, error="File not found"), 404

    try:
        return jsonify(success=True)
    
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500
    
# TO DO : REFACTOR ALL FOR REACT
@insights_bp.route('/sheets', methods=['POST'])
def view_cleaned_sheets():
    return render_template('cleaned_sheets.html', sheets=cleaned_data)

@insights_bp.route('/select_sheet', methods=['POST'])
def select_sheet():
    selected_sheet = request.form.get('selected_sheet')
    
    if not selected_sheet:
        return "No sheet selected. Please go back.", 400
    
    session['selected_sheet'] = selected_sheet
    return redirect(url_for('select_insight'))


@insights_bp.route('/insights', methods = ['GET', 'POST'])
def select_insight():
    if request.method == 'POST':
        # Final insight form submission (second form)
        selected_sheet = session.get('selected_sheet')
        insight = request.form.get('insight')
        sub_insight = request.form.get('sub_insight')

        sheet_df = cleaned_data.get(selected_sheet)
        chart_path = build_chart_filename(insight, sub_insight, selected_sheet)
        print(chart_path)

        ''' For debugging:
        print("POSTED DATA:")
        print("insight:", insight)
        print("sub_insight:", sub_insight)
        print("selected_sheet:", selected_sheet) '''

        if insight == 'peak_times':
            visualise_peak_transaction_times(sheet_df, save_path=chart_path)

        elif insight == 'popular_items':
            if sub_insight == 'popular_by_transactions':
                visualise_most_popular_by_num_transactions(sheet_df, top_n=10, save_path=chart_path)
            elif sub_insight == 'popular_by_quantity':
                visualise_most_popular_by_quantity(sheet_df, top_n=10, save_path=chart_path)

        elif insight == 'highest_revenue':
            visualise_highest_revenue_items(sheet_df, top_n=10, save_path=chart_path)

        else:
            return "Invalid selection", 400

        chart_filename = os.path.relpath(chart_path, start='static')
        chart_filename = chart_filename.replace("\\", "/")  # Ensures browser-safe forward slashes

        print("Relative chart filename for HTML:", chart_filename)

        title = get_insight_title(insight, sub_insight)
        return render_template('insight_result.html', chart_filename=chart_filename, insight_title=title)
    
    else:  # This is the GET request — when user first arrives at /insights
        print("Back here again")
        selected_sheet = session.get('selected_sheet')
        return render_template('insights.html', selected_sheet=selected_sheet)

@insights_bp.route('/charts/<filename>')
def serve_chart(filename):
    return send_from_directory(os.path.abspath('static/charts'), filename)