import os
import json
import csv
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

# ---------------------------------------------------------------------------
# Use absolute paths so the app works regardless of the working directory
# the server is launched from (important for Gunicorn on cloud platforms).
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)

# Load model parameters
with open(os.path.join(BASE_DIR, 'model_parameters.json'), 'r') as f:
    model_params = json.load(f)


def load_car_data():
    companies = set()
    years = set()
    fuel_types = set()
    company_models = {}

    csv_path = os.path.join(BASE_DIR, 'Cleaned_Car_data.csv')
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            if not row or len(row) < 7:
                continue
            name = row[1]
            company = row[2]
            year = int(row[3])
            fuel = row[6]
            
            companies.add(company)
            years.add(year)
            fuel_types.add(fuel)
            
            if company not in company_models:
                company_models[company] = set()
            company_models[company].add(name)

    return (
        sorted(list(companies)),
        sorted(list(years), reverse=True),
        sorted(list(fuel_types)),
        {comp: sorted(list(models)) for comp, models in company_models.items()}
    )


@app.route('/', methods=['GET'])
def index():
    companies, years, fuel_types, company_models = load_car_data()
    return render_template(
        'index.html',
        companies=companies,
        company_models=json.dumps(company_models),
        years=years,
        fuel_types=fuel_types,
    )


@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    company   = request.form.get('company', '').strip()
    car_model = request.form.get('car_models', '').strip()
    year      = request.form.get('year', '').strip()
    fuel_type = request.form.get('fuel_type', '').strip()
    driven    = request.form.get('kilo_driven', '').strip()

    # --- Input validation ---------------------------------------------------
    if not all([company, car_model, year, fuel_type, driven]):
        return 'Please fill in all fields.', 400

    try:
        year_int   = int(year)
        driven_int = int(driven)
    except ValueError:
        return 'Year and Kilometers Driven must be valid numbers.', 400

    # --- Prediction ---------------------------------------------------------
    try:
        # Linear regression calculation in pure python:
        prediction = model_params['intercept']
        prediction += model_params['coef_name'].get(car_model, 0.0)
        prediction += model_params['coef_company'].get(company, 0.0)
        prediction += model_params['coef_fuel_type'].get(fuel_type, 0.0)
        prediction += model_params['coef_year'] * year_int
        prediction += model_params['coef_kms_driven'] * driven_int

        # Round to 2 decimal places
        prediction_rounded = round(prediction, 2)
        return str(prediction_rounded)
    except Exception as e:
        # Log the real error server-side; return a clean message to the client
        print(f'Prediction error: {e}')
        return 'Could not generate a prediction. Please try different inputs.', 500


if __name__ == '__main__':
    # Dev only — Gunicorn takes over in production (via Procfile)
    app.run(debug=True)