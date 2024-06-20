from flask import Flask, jsonify, Response, make_response
from flask_cors import CORS

from bank import models
from bank.loader import get_problems_dict
from classes.difficulty.main import difficulty_gen
from classes.recommender.main import recommend_problem

app = Flask(__name__)
CORS(app)

problems_dict: dict[str, models.Problem] = {}
user_history: list[tuple[str, bool]] = []


@app.route('/problems/<string:pid>', methods=['GET'])
def get_data(pid: str) -> Response:
    return jsonify(problems_dict[pid])


@app.route('/history/<string:pid>/<int:solved>', methods=['PATCH'])
def patch_problem_history(pid: str, solved: int) -> Response:
    found = False

    for i in range(len(user_history)):
        if user_history[i][0] == pid:
            user_history[i] = (pid, bool(solved))
            found = True
            break

    if not found:
        user_history.append((pid, bool(solved)))

    return make_response('ok', 201)


@app.route('/recommend', methods=['GET'])
def get_recommended_problem() -> Response:
    problem, similarity = recommend_problem(history_data=user_history)
    difficulty = difficulty_gen(problem)

    return jsonify({
        'problem': problem,
        'similarity': similarity,
        'difficulty': difficulty,
    })


if __name__ == '__main__':
    problems_dict = get_problems_dict()
    app.run(host='0.0.0.0', port=6610, debug=True)
