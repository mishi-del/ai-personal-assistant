from flask import Flask, render_template, request, jsonify
import os
from agent import AIAgent
from config import default_config

app = Flask(__name__)
agent = AIAgent()

# Ensure the templates directory exists
os.makedirs('templates', exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message', '')
    if user_message:
        response = agent.process_command(user_message)
        return jsonify({'response': response})
    return jsonify({'response': 'No message received'})

if __name__ == '__main__':
    # Run on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True) 