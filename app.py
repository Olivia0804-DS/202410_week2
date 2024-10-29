from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# Store chat history in memory (in a real app, you'd use a database)
chat_history = []

# Some educational responses for teaching Python concepts
PYTHON_CONCEPTS = {
    "loop": "In Python, loops (for and while) are used for iteration. Example: for i in range(5): print(i)",
    "list": "Lists are ordered collections in Python. Example: my_list = [1, 2, 3]. You can append, remove, and modify elements.",
    "dictionary": "Dictionaries store key-value pairs. Example: my_dict = {'name': 'John', 'age': 25}",
    "function": "Functions are defined using 'def'. Example: def greet(name): return f'Hello {name}!'",
    "class": "Classes are blueprints for objects. Example: class Dog: def bark(self): return 'Woof!'"
}

@app.route('/')
def hello_world():
    return '''
    Welcome to the Python Learning Chat!
    Available endpoints:
    - /chat?message=your_message
    - /history
    - /learn?topic=python_concept
    '''

@app.route('/chat')
def chat():
    message = request.args.get('message', '').lower()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Process the message and generate a response
    response = process_message(message)
    
    # Store in chat history
    chat_entry = {
        'timestamp': timestamp,
        'message': message,
        'response': response
    }
    chat_history.append(chat_entry)
    
    # Return JSON response
    return jsonify(chat_entry)

def process_message(message):
    # Check for Python keywords in the message
    for concept, explanation in PYTHON_CONCEPTS.items():
        if concept in message:
            return f"Let me teach you about {concept}: {explanation}"
    
    # Basic conversation patterns
    if "hello" in message or "hi" in message:
        return "Hello! What would you like to learn about Python today?"
    elif "help" in message:
        return "I can help you learn about Python concepts! Try asking about: loops, lists, dictionaries, functions, or classes."
    elif "example" in message:
        return provide_random_example()
    else:
        return f"You said: {message}. Try asking about Python concepts or type 'help' for guidance!"

@app.route('/history')
def get_history():
    # Add option to limit the number of messages returned
    limit = request.args.get('limit', default=10, type=int)
    return jsonify(chat_history[-limit:])

@app.route('/learn')
def learn():
    topic = request.args.get('topic', '').lower()
    if topic in PYTHON_CONCEPTS:
        return jsonify({
            'topic': topic,
            'explanation': PYTHON_CONCEPTS[topic]
        })
    else:
        return jsonify({
            'error': 'Topic not found',
            'available_topics': list(PYTHON_CONCEPTS.keys())
        })

def provide_random_example():
    examples = [
        "Here's a list comprehension example: squares = [x**2 for x in range(5)]",
        "Here's a lambda function example: add = lambda x, y: x + y",
        "Here's a string formatting example: name = 'World'; print(f'Hello {name}!')",
        "Here's a try/except example: try:\n    result = 10/0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')"
    ]
    return random.choice(examples)



#http://localhost:5000/chat?message=tell+me+about+lists
#http://localhost:5000/history?limit=5
#http://localhost:5000/learn?topic=dictionary

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)