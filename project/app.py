from flask import Flask, request, jsonify, render_template
import re
import random

app = Flask(__name__)

response = {
    "hello": ["Hello, how can I assist you?"],
    "hi": ["Hello, how can I help you?"],
    "hey": ["Hello, how can I assist you?"],
    "hai": ["Hello, how can I help you?"],
    "i feel (.*)": ["Why do you feel {}?", "How long have you been feeling {}?"],
    "i am (.*)": ["Why do you say you're {}?", "How long have you been {}?"],
    "i have been (.*) for (.*)":["why do you say you're feeling like that"],
    "i've been (.*) for (.*)":["why do you say you're feeling like that"],
    "i'm (.*)": ["Why are you {}?", "How long have you been {}?"],
    "i(.*) you": ["Why do you {} me?", "What makes you think you {} me?"],
    "i (.*) myself": ["Why do you {} yourself?", "What makes you think you {} yourself?"],
    "cause i am not (.*) enough":["Why do you think you are not {} enough"],
    "(.*) sorry (.*)": ["There is no need to apologize.", "What are you apologizing for?"],
    "(.*) friend (.*)": ["Tell me more about your friend.", "How do your friends make you feel?"],
    "yes": ["You seem quite sure.", "Okay, can you elaborate?"],
    "no": ["Why not?", "Okay, but can you elaborate a bit?"],
    "(.*) ": ["Please tell me more.", "Let's change focus a bit... Tell me about your family.", "Can you elaborate?"],
    " ": ["Why do you think that?", "Please tell me more.", "Let's change focus a bit... Tell me about your family.", "Can you elaborate?"],
    "I dont like (.*)": ["why do you not like {}"],

}

def match_response(input_text):
    for pattern, response_list in response.items():
        matches = re.match(pattern, input_text.lower())
        if matches:
            chosen_response = random.choice(response_list)
            return chosen_response.format(*matches.groups())
    return "I'm so sorry, I don't understand what you're saying."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.get_json().get("message")
    if user_input is None:
        return jsonify({"error": "Invalid request"}), 400
    response_text = match_response(user_input)
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
