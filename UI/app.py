from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/components', methods=['GET'])
def get_components():
    return jsonify({
        'agents': ['Agent1', 'Agent2', 'Agent3'],
        'tools': ['Tool1', 'Tool2', 'Tool3']
    })

@app.route('/api/create_agency', methods=['POST'])
def create_agency():
    data = request.json
    # Process the agency configuration
    # This is where you'd integrate with your agentic framework
    return jsonify({'message': 'Agency created successfully', 'config': data})

if __name__ == '__main__':
    app.run(debug=True)