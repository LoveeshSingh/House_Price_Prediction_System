from flask import Flask, request, jsonify, render_template
import pickle
import json
import numpy as np
import pandas as pd

app = Flask(__name__)

model = pickle.load(open('bangalore_home_prices_model.pickle', 'rb'))

columns = json.load(open('columns.json'))['data_columns']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form['location']
    sqft = float(request.form['sqft'])
    bath = int(request.form['bath'])
    bhk = int(request.form['bhk'])

    x = np.zeros(len(columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if location in columns:
        loc_index = columns.index(location)
        x[loc_index] = 1

    df = pd.DataFrame([x], columns=columns)
    price = model.predict(df)[0]

    return jsonify({'price': round(price, 2)})

if __name__ == '__main__':
    app.run(debug=True)
