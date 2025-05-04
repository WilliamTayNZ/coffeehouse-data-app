# Imports

# render_template: 	To render HTML templates like index.html
# request: To handle form data and file uploads
# redirect, url_for: To navigate between routes after actions (e.g., redirect after upload)
  # redirect redirects the browser to a different URL (HTTP 302) 
  # url_for generates the URL for a specific Flask view (route) based on its function name

# secure_filename: To sanitize uploaded file names (strips risky characters or paths) and prevent path injection
# os: For working with file paths and upload folders
# clean_excel_sheets: Cleaning function that processes the uploaded Excel file

# UPLOAD_FOLDER: Tells Flask where to save incoming .xlsx files
# os.makedirs(UPLOAD_FOLDER, exist_ok=True) Ensures the folder exists; creates it if not. exist_ok ensures no error when already exist



# Flask and werkzeug

# Flask is a lightweight web framework
# werkzeug is the underlying library Flask uses to handle things like: HTTP requests and responses, routing, file uploads, sessions etc

from flask import render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from app.cleaner import clean_excel_sheets
from app.insights import (
    visualise_peak_transaction_times,
    visualise_most_popular_by_num_transactions,
    visualise_most_popular_by_quantity,
    visualise_highest_revenue_items
)
from app.utils import (build_chart_filename, get_insight_title)
from app.utils import CHART_FOLDER
                       

# Define where uploaded files are stored
UPLOAD_FOLDER = 'uploads' 

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)


# In-memory storage for cleaned data
cleaned_data = {}

from flask import send_from_directory



def register_routes(app):

    @app.route('/', methods = ['GET', 'POST']) # methods is built-in to Flask's route decorator, represents HTTP methods
    def upload_file():
        if request.method == 'POST': # request is a Flask object representing the current HTTP request, method is built-in property
            file = request.files['file'] # request.files is a Flask/Werkzeug dictionary-like object that holds uploaded files
            if file and file.filename.endswith('.xlsx'): # Checks if file is truthy
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                global cleaned_data # necessary to call 
                cleaned_data, cleaning_summary = clean_excel_sheets(filepath)

                return render_template('cleaning_summary.html', summary=cleaning_summary)
            
        else:
            return render_template('index.html')
        

    @app.route('/sheets', methods=['POST'])
    def view_cleaned_sheets():
        return render_template('cleaned_sheets.html', sheets=cleaned_data)
    
    @app.route('/select_sheet', methods=['POST'])
    def select_sheet():
        selected_sheet = request.form.get('selected_sheet')
        
        if not selected_sheet:
            return "No sheet selected. Please go back.", 400
        
        session['selected_sheet'] = selected_sheet
        return redirect(url_for('select_insight'))
    
        
    @app.route('/insights', methods = ['GET', 'POST'])
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
        
    @app.route('/charts/<filename>')
    def serve_chart(filename):
        return send_from_directory(os.path.abspath('static/charts'), filename)
        


# Future suggestion: image.png








