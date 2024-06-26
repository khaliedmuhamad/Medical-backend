# analysis_script.py
import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
print ("JA2")
@app.route('/analyze', methods=['POST','GET'])
def analyze():
    file = request.files['dicom']
   
    result = {"message": "DICOM analysis result_2"} 
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
