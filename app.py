from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load models
rf_model = joblib.load('random_forest_model.pkl')
svm_model = joblib.load('svm_model.pkl')
log_reg_model = joblib.load('logistic_regression_model.pkl')

FEATURE_COLUMNS = [
    'gender', 'ssc_p', 'hsc_p', 'degree_p', 'etest_p', 'mba_p',
    'ssc_b_Central', 'ssc_b_Others', 'hsc_b_Central', 'hsc_b_Others',
    'hsc_s_Arts', 'hsc_s_Commerce', 'hsc_s_Science',
    'degree_t_Comm&Mgmt', 'degree_t_Others', 'degree_t_Sci&Tech',
    'workex_No', 'workex_Yes', 'specialisation_Mkt&Fin', 'specialisation_Mkt&HR'
]

def preprocess_input(data):
    df = pd.DataFrame([data])
    df = df.reindex(columns=FEATURE_COLUMNS, fill_value=0)
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = preprocess_input(data)
    
    rf_pred = rf_model.predict(df)[0]
    svm_pred = svm_model.predict(df)[0]
    log_reg_pred = log_reg_model.predict(df)[0]
    
    prediction_labels = {0: 'Not Placed', 1: 'Placed'}
    
    response = {
        'Random Forest': prediction_labels[rf_pred],
        'SVM': prediction_labels[svm_pred],
        'Logistic Regression': prediction_labels[log_reg_pred]
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
