import os
import json
import pickle

import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

# ---------------------------------------------------------------------------
# Use absolute paths so the app works regardless of the working directory
# the server is launched from (important for Gunicorn on cloud platforms).
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)

model = pickle.load(open(os.path.join(BASE_DIR, 'LinearRegressionModel.pkl'), 'rb'))
car   = pd.read_csv(os.path.join(BASE_DIR, 'Cleaned_Car_data.csv'))


@app.route('/', methods=['GET'])
def index():
    companies  = sorted(car['company'].unique())
    years      = sorted(car['year'].unique(), reverse=True)
    fuel_types = car['fuel_type'].unique()

    # Exact company -> [models] map — avoids substring false-positives in JS
    company_models = {
        company: sorted(car[car['company'] == company]['name'].unique().tolist())
        for company in companies
    }

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
        df = pd.DataFrame(
            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
            data=[[car_model, company, year_int, driven_int, fuel_type]],
        )
        prediction = model.predict(df)
        return str(np.round(prediction[0], 2))
    except Exception as e:
        # Log the real error server-side; return a clean message to the client
        print(f'Prediction error: {e}')
        return 'Could not generate a prediction. Please try different inputs.', 500


if __name__ == '__main__':
    # Dev only — Gunicorn takes over in production (via Procfile)
    app.run(debug=True)