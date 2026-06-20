from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
prediction_history = []

# Load ML files
severity_model = joblib.load("severity_model.pkl")
risk_model = joblib.load("risk_model.pkl")
scaler = joblib.load("scaler.pkl")
severity_encoder = joblib.load("severity_encoder.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# Load dataset
df = pd.read_csv("indian_roads_dataset.csv")

# Dashboard values
total_accidents = len(df)
high_risk = len(df[df["accident_severity"].isin(["fatal", "major"])])
total_casualties = int(df["casualties"].sum())
average_risk = round(df["risk_score"].mean(), 2)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    # Weather
    weather_labels = df["weather"].value_counts().index.tolist()
    weather_values = df["weather"].value_counts().values.tolist()

    # Road Type
    road_labels = df["road_type"].value_counts().index.tolist()
    road_values = df["road_type"].value_counts().values.tolist()

    # Severity
    severity_labels = df["accident_severity"].value_counts().index.tolist()
    severity_values = df["accident_severity"].value_counts().values.tolist()

    # Top Cities
    city_labels = df["city"].value_counts().head(5).index.tolist()
    city_values = df["city"].value_counts().head(5).values.tolist()

    # Hour Wise
    hour_labels = list(range(24))
    hour_values = (
        df["hour"]
        .value_counts()
        .reindex(hour_labels, fill_value=0)
        .tolist()
    )

    return render_template(
        "dashboard.html",
        total_accidents=total_accidents,
        high_risk=high_risk,
        total_casualties=total_casualties,
        average_risk=average_risk,
        weather_labels=weather_labels,
        weather_values=weather_values,
        road_labels=road_labels,
        road_values=road_values,
        severity_labels=severity_labels,
        severity_values=severity_values,
        city_labels=city_labels,
        city_values=city_values,
        hour_labels=hour_labels,
        hour_values=hour_values,
        history=prediction_history,
    )


@app.route("/predict", methods=["POST"])
def predict():

    values = []

    for col in feature_columns:
        values.append(float(request.form[col]))

    values = np.array(values).reshape(1, -1)

    values = scaler.transform(values)

    severity = severity_model.predict(values)[0]
    severity = severity_encoder.inverse_transform([severity])[0]

    risk = risk_model.predict(values)[0]

    prediction_history.append({
    "severity": severity,
    "risk": round(risk, 2)
})

    return render_template(
        "index.html",
        severity=severity,
        risk=round(risk, 2)
    )

from flask import Response
import csv
import io

@app.route("/download")
def download():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["#", "Severity", "Risk Score"])
    for i, item in enumerate(prediction_history, 1):
        writer.writerow([i, item["severity"], item["risk"]])
    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=predictions.csv"}
    )

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)