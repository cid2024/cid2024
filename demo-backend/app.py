from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask backend!")

@app.route('/problems/<string:id>', methods=['GET'])
def get_data(id):
    return jsonify({
        "id": id,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6610, debug=True)
