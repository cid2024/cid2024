from flask import Flask, jsonify, Response
from flask_cors import CORS

from bank import models
from bank.loader import get_problems_dict

app = Flask(__name__)
CORS(app)

problems_dict: dict[str, models.Problem] = {}


@app.route('/problems/<string:id>', methods=['GET'])
def get_data(id: str) -> Response:
    return jsonify(problems_dict[id])


if __name__ == '__main__':
    problems_dict = get_problems_dict()
    print(problems_dict.keys())
    app.run(host='0.0.0.0', port=6610, debug=True)
