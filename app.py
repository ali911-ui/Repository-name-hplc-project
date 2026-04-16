from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Dummy dataset (you will expand later)
compounds = [
    {"name": "Compound A", "rt": 5.0, "phi": 0.6, "sigma": 0.5},
    {"name": "Compound B", "rt": 7.2, "phi": 0.7, "sigma": 1.2},
    {"name": "Compound C", "rt": 3.8, "phi": 0.5, "sigma": -0.3},
]

# Simplified Snyder-like model
def predict_rt(phi, S=5):
    return S * phi

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    user_phi = data.get("phi")   # solvent proportion
    user_rt = data.get("rt")     # retention time
    
    results = []

    for compound in compounds:
        predicted = predict_rt(user_phi)
        
        # error calculation
        error = abs(predicted - compound["rt"])
        
        results.append({
            "name": compound["name"],
            "predicted_rt": round(predicted, 2),
            "error": round(error, 2)
        })
    
    # sort by closest match
    results = sorted(results, key=lambda x: x["error"])
    
    return jsonify(results[:3])  # top 3 matches

if __name__ == '__main__':
    app.run(debug=True)