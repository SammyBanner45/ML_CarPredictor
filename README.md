# 🚗 Car Price Predictor

A machine learning web app that predicts the **resale price of a used car** based on its brand, model, year of manufacture, fuel type, and kilometres driven.

Built with **Flask** + **scikit-learn** (Linear Regression), styled with a clean light-blue and white theme.

---

## ✨ Features

- Instant ML-powered price prediction
- Dropdown menus auto-filtered by company → model
- Input validation on both client and server
- Clean, responsive UI with watermark car icon
- Production-ready with Gunicorn

---

## 🖼️ Preview

> Select a company, pick a model, set the year, fuel type and km driven — get an estimated resale price in seconds.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11, Flask 3.x |
| ML Model | scikit-learn Linear Regression |
| Data | Cleaned Indian used-car market CSV |
| Frontend | HTML5, Vanilla CSS, Vanilla JS |
| Production | Gunicorn (WSGI) |

---

## 🚀 Running Locally

### 1. Clone the repo

```bash
git clone https://github.com/SammyBanner45/ML_CarPredictor.git
cd ML_CarPredictor
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dev server

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## ☁️ Deploying to Render (Free)

1. Push this repo to GitHub (already done ✅)
2. Go to [render.com](https://render.com) → **New** → **Web Service**
3. Connect your GitHub repo
4. Render auto-detects the `Procfile` and sets the start command to `gunicorn app:app`
5. Click **Deploy** — your app will be live in ~2 minutes

> **Note:** The `LinearRegressionModel.pkl` and `Cleaned_Car_data.csv` files are committed to the repo and served directly by the app. No external database needed.

---

## 📁 Project Structure

```
ML_CarPredictor/
├── app.py                    # Flask app — routes and prediction logic
├── LinearRegressionModel.pkl # Trained scikit-learn pipeline
├── Cleaned_Car_data.csv      # Source data (Indian used-car listings)
├── requirements.txt          # Python dependencies
├── Procfile                  # Gunicorn start command (for Render/Heroku)
├── runtime.txt               # Python version pin
├── favicon.png               # App icon
├── templates/
│   └── index.html            # Jinja2 HTML template
└── static/
    ├── favicon.png           # Served favicon
    └── css/
        └── style.css         # Styles (#69C4FB / white theme)
```

---

## 🤖 Model Details

- **Algorithm:** Linear Regression (via scikit-learn `Pipeline`)
- **Features:** Car name, Company, Year, Kilometres driven, Fuel type
- **Preprocessing:** `OneHotEncoder` for categorical columns via `ColumnTransformer`
- **Training data:** Indian used-car listings (cleaned)

---

## 📄 License

MIT