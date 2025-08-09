# mock_server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/chat/completions', methods=['POST'])
def chat_completions():
    return jsonify({
        "model": "llama3.1:8b",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response from the model."
                }
            }
        ],
        "usage": {
            "total_duration": 1200,
            "load_duration": 200,
            "response_token/s": 20,
            "prompt_token/s": 50,
            "eval_count": 100,
            "completion_tokens": 30
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=42004)

