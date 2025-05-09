from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import json


url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqiwcRAJ3JlylV18B85B21gSgodfCidSptZp2fV6m16NIp4gy5Ol6mddqC5GLHF_hVM0lUOBo57c0s/pub?gid=0&single=true&output=csv"
k = 4

df = pd.read_csv(url)

# Declare the APP server instance
app = Flask(__name__)
# Enable CORS policies
CORS(app)

# GET Endpoint =============================================================================
@app.route("/", methods=["GET"])
def index():
  return jsonify({"msg": "Hello Python REST API"})

# POST Endpoint =============================================================================
@app.route('/post_endpoint', methods=['POST'])
def create_data():
    # Get the data from the POST endpoint
    data = request.get_json()
    if not data:
        return (jsonify({'error': 'No data provided'}), 400)
    return (jsonify({'response': 'ok all good'}), 201)

@app.route('/names', methods=['GET'])
def get_names():
    # Get the names from the DataFrame
    names = df['Nombre completo'].tolist()
    return (jsonify(names), 200)

@app.route('/pizza', methods=['POST'])
def select_pizza_budies():
  data = request.get_json()

  if not data:
    return (jsonify({'error': 'No data provided'}), 400)
   
  selected_name = data.get('name')
  selected_person = df[df['Nombre completo'] == selected_name].iloc[:, 1:].values[0] 

  similarities = []
   
  for _, row in df.iterrows():
    other_name = row['Nombre completo']
    if other_name == selected_name:
        continue
    
    other_person = row.iloc[1:].values  # Exclude name
    dot_product = np.dot(selected_person, other_person)
    magnitude1 = np.linalg.norm(selected_person)
    magnitude2 = np.linalg.norm(other_person)

    similarity = dot_product / (magnitude1 * magnitude2)
    similarities.append((other_name, similarity))

      # Sort and get top K
      
  top_k = sorted(similarities, key=lambda x: x[1], reverse=True)[:k]
  return jsonify(top_k), 200
   

# Execute the app instance
# The app will run locally in: http://localhost:5001/ after execution
if __name__ == "__main__":
  import os

  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
