from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Function to predict marks
def predict_marks(user_data):
    df = pd.DataFrame([user_data])
    marks = (
        0.3 * df['Previous_Sem_Percentage'] +
        0.45 * (df['Hours_Studied'].clip(0, 10) / 10 * 100)  -
        0.2 * df['Phone_Usage_Hrs'] -
        0.5 * df['Subject_Difficulty'] -
        0.25 * df['Test_Anxiety_Level'] +
        np.random.normal(0, 2, len(df))
    )
    marks = marks.clip(0, 100)
    return round(marks.values[0], 2)


# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Chat/predict route for JS
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    # Convert all inputs to float
    for k in data:
        data[k] = float(data[k])
    pred = predict_marks(data)
    return jsonify({"reply": f"Predicted Marks: {pred}"})

if __name__ == "__main__":
    app.run(debug=True)
