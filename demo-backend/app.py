from flask import Flask, jsonify
from bank import models
from bank.loader import get_problems_dict

app = Flask(__name__)

problems_dict: dict[str, models.Problem] = {}

@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask backend!")

@app.route('/problems/<string:id>', methods=['GET'])
def get_data(id):
    return jsonify(problems_dict[id])

if __name__ == '__main__':
    problems_dict = get_problems_dict()
    app.run(host='0.0.0.0', port=6610, debug=True)
