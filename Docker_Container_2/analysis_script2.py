# analysis_script.py
import os
import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Liste möglicher realistischer Diagnoseergebnisse
diagnoses = [
    "Fraktur des Femurs",
    "Lungenentzündung",
    "Kardiomegalie",
    "Hirntumor",
    "Leberzirrhose",
    "Osteoarthritis",
    "Akute Appendizitis",
    "Pulmonale Embolie",
    "Metastatische Krebserkrankung",
    "Chronische Niereninsuffizienz"
]

@app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    file = request.files.get('dicom')
    
    if file:
        # Zufällige Diagnose auswählen
        result = {"diagnosis": random.choice(diagnoses)}
        return jsonify(result)
    else:
        return jsonify({"error": "No DICOM file provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
