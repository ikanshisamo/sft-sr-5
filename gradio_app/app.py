from flask import Flask, render_template, request, jsonify
from logic import chat, SYSTEM_PROMPTS, CHOICE_TO_MODE

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/prompts', methods=['GET'])
def api_prompts():
    return jsonify({"status": "success", "prompts": SYSTEM_PROMPTS})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    user_message = data.get("message", "")
    history = data.get("history", [])
    emotion = data.get("emotion", "")

    # BACA system_prompt LANGSUNG DARI REQUEST JSON (Frontend)
    system_prompt = data.get("system_prompt", "") 

    response_text = ""
    updated_history = []
    
    try:
        # Panggil logic.py dengan parameter konstan untuk token dan temperature
        for _, current_history in chat(user_message, history, system_prompt, 0.7, 8192, emotion):
            updated_history = current_history
            
        if updated_history:
            response_text = updated_history[-1]["content"]

        return jsonify({
            "status": "success", 
            "response": response_text,
            "history": updated_history
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)