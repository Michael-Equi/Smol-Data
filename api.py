from flask import Flask, request
from flask_cors import CORS
import json

from controller import Controller
from utils import text_to_html

app = Flask(__name__)
CORS(app)

controller = Controller()
controller.load_data()


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
    
    if len(messages) == 0:
        return json.dumps({'error': 'Invalid request body. "messages" is empty.'}), 400


    last_message = messages[-1]
    role = last_message.get('role')

    if role != 'user':
        return json.dumps({'error': 'Invalid request body. Last message must be from user.'}), 400

    text = last_message.get('text')
    if text is None:
        return json.dumps({'error': 'Invalid request body. Last message must have text.'}), 400


    plan = controller.plan(text)
    html = text_to_html(plan)

    messages.append({
        'role': 'assistant',
        'text': html
    })

    print(messages)

    return json.dumps({"messages": messages}), 200



if __name__ == "__main__":
    app.run(port=8000, debug=True)