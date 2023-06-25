from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Index</p>"


@app.route("/api/input", methods=['POST'])
def controller_input():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return json.dumps({'error': 'Invalid content type'}), 400

    data = request.json
    messages = data.get('messages')
    
    if messages is None:
        return json.dumps({'error': 'Invalid request body. Missing key "messages".'}), 400

    return json.dumps(messages), 200



if __name__ == "__main__":
    app.run(port=8000, debug=True)