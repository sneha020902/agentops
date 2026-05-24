from flask import Flask, request, jsonify, send_from_directory
from agent import run_agent

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    query = request.json.get('query', 'Why did my latest pipeline fail?')
    result = run_agent(query)
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
