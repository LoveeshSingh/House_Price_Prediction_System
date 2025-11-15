# House Price Prediction System

A full‑stack Machine Learning web application that predicts house prices (in Lakhs) for Bangalore using location, square footage, number of bathrooms, and BHK count.

- Frontend: Netlify (static HTML/CSS/JS)
- Backend API: Flask + Scikit-Learn deployed on Render
- ML model: Linear Regression trained on the Bangalore House Prices dataset

Live demo
- Frontend (Netlify): https://house-price-prediction-system.netlify.app
- Backend API (Render): https://house-price-api-s8b3.onrender.com  
  Note: Render free‑tier instances may take ~20 seconds to wake up.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [API](#api)
- [Sample Requests](#sample-requests)
- [How it works / ML details](#how-it-works--ml-details)
- [Project Structure](#project-structure)
- [Run Locally](#run-locally)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [Retrain the Model](#retrain-the-model)
- [Deployment Notes](#deployment-notes)
- [Testing Scenarios](#testing-scenarios)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements & Credits](#acknowledgements--credits)
- [Contact](#contact)

---

## Features

- 🔮 Real‑time house price prediction
- 📍 Location‑aware inputs via one‑hot encoded features
- 🧠 Linear Regression model trained on real Bangalore house-price data
- 🚀 Deployed: Flask backend (Render) + Static frontend (Netlify)
- 🔗 CORS enabled for smooth API integration
- 🎨 Clean, centered UI with dark theme

---

## Tech Stack

- Backend: Python, Flask, Flask‑CORS
- ML: NumPy, Pandas, Scikit‑Learn
- Serialization: pickle (model) + JSON (column index)
- Deployment: Render (API), Netlify (frontend)
- Frontend: HTML, CSS, JavaScript (fetch/XHR)

---

## API

Base URL: `https://house-price-api-s8b3.onrender.com`

Endpoint
- POST `/predict`
  - Form fields (application/x-www-form-urlencoded or form-data):
    - `location` (string) — name of the locality (example: "Indira Nagar")
    - `sqft` (number) — built up area in square feet (example: 1600)
    - `bath` (number) — number of bathrooms (example: 3)
    - `bhk` (number) — number of bedrooms (example: 3)
  - Response (JSON):
    - `predicted_price` (number) — predicted price in Lakhs
    - Example:
      {
        "predicted_price": 123.45
      }

Notes:
- The backend expects `location` to match one of the locations in the model's column index. If a location is unseen, the backend falls back to treating it as a zero vector for location columns (model behavior depends on implementation).
- CORS is enabled so frontend hosted on Netlify can call the API on Render.

---

## Sample Requests

Curl example:
```bash
curl -X POST "https://house-price-api-s8b3.onrender.com/predict" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "location=Koramangala&sqft=1600&bath=3&bhk=3"
```

JavaScript (fetch) example:
```javascript
fetch("https://house-price-api-s8b3.onrender.com/predict", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({
    location: "Koramangala",
    sqft: 1600,
    bath: 3,
    bhk: 3
  })
})
.then(res => res.json())
.then(data => console.log("Predicted price (Lakhs):", data.predicted_price));
```

---

## How it works / ML details

- Algorithm: Linear Regression
- Dataset: Bangalore House Prices dataset (public dataset commonly used for price prediction tutorials)
- Preprocessing:
  - Cleaned `sqft` values and converted ranges to numeric averages where needed
  - Removed outliers (extreme sqft or price per sqft)
  - Ensured consistency for `bhk` and `bath` values
- Location encoding: One‑hot encoding (columns saved in a JSON column index)
- Artifacts:
  - `model.pkl` — serialized trained model (pickle)
  - `column_index.json` — list of feature column names used during training

If you want to retrain, see the [Retrain the Model](#retrain-the-model) section.

---

## Project Structure

A typical layout (your repo may vary):

- backend/
  - app.py                # Flask app with /predict endpoint
  - model.pkl             # Serialized trained model
  - columns.json          # Column index / feature mapping
  - requirements.txt
  - utils.py              # helpers for preprocessing & prediction
- frontend/
  - index.html
  - static/
    - css/
    - js/
- notebooks/
  - training.ipynb        # data cleaning, feature engineering, model training
- README.md

---

## Run Locally

Prerequisites:
- Python 3.8+
- Node / npm (optional, only if you want to run a dev server for the frontend)
- Virtualenv recommended

### Backend (Flask)

1. Clone the repo
```bash
git clone <repo-url>
cd <repo-root>/backend
```

2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate.bat  # Windows

pip install -r requirements.txt
```

3. Ensure model artifacts exist in the backend folder:
- `model.pkl`
- `columns.json` (or `column_index.json` depending on the repo)

4. Run the Flask app
```bash
# For development
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000

# Or directly
python app.py

# Production-style (Gunicorn)
gunicorn app:app --bind 0.0.0.0:8000
```

The API will be available at http://127.0.0.1:5000 or the port you specified.

### Frontend

The frontend is static; you can serve it by opening `frontend/index.html` in a browser or run a simple HTTP server:

```bash
cd frontend
# Python 3
python -m http.server 3000
# Visit http://localhost:3000
```

If the frontend expects the API at a different URL, update the JS fetch URL to point at your local backend (e.g., http://localhost:5000/predict).

### Retrain the Model

1. Open `notebooks/training.ipynb`
2. Follow the notebook to:
   - Load and clean the Bangalore dataset
   - Engineer features
   - Fit a LinearRegression model
   - Save `model.pkl` and `columns.json` (or update filenames used by the backend)
3. Export artifacts and replace files in `backend/` with the newly trained ones.

Important: Keep the feature column ordering consistent with `columns.json` the backend uses.

---

## Deployment Notes

- Backend: Render (or any WSGI host). Use Gunicorn for production. Make sure the `model.pkl` and `columns.json` are included in the deployed repository and the working directory.
- Frontend: Netlify for static hosting. Ensure `index.html` fetch URL points to the deployed backend.
- If using Render free tier, the API may sleep when idle; cold starts may take ~20s.

CI/CD:
- GitHub pushes can auto‑trigger new deployments for Netlify and Render if configured.

---

## Testing Scenarios

Try these example inputs on the live demo or local instance:

Premium Areas
- Indira Nagar — 1800 sqft, 3 bath, 3 bhk → Very high price
- Koramangala — 1600 sqft, 3 bath, 3 bhk → High price

Mid-Range
- Whitefield — 1200 sqft, 2 bath, 2 bhk → Medium price
- JP Nagar — 1000 sqft, 2 bath, 2 bhk → Medium price

Low-Cost
- Electronic City — 700 sqft, 1 bath, 1 bhk → Low price

---

## Contributing

Contributions are welcome. Suggested workflow:
1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make changes and add tests if applicable
4. Commit and push: `git push origin feat/your-feature`
5. Open a Pull Request with a descriptive title and details

Please ensure:
- Model artifacts are not inadvertently retrained and committed unless intended
- Large binary files (like models) follow your project's LFS policy if needed

---

## License

This project is provided under the MIT License. See the LICENSE file for details.

---

## Acknowledgements & Credits

- Bangalore House Prices dataset (many public variants available online)
- Inspired by common ML deployment patterns and Flask + Netlify tutorials

---

## Contact

Maintainer: LoveeshSingh (GitHub: @LoveeshSingh)

If you need help setting up, retraining the model, or deploying, open an issue or reach out via GitHub.
