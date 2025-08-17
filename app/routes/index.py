from flask import Blueprint, render_template

# -------------------------

index_bp = Blueprint('index', __name__)

# -------------------------

conversation = [
    {
        'id': 1,
        'role': 'user',
        'content': 'Hello! Are you a human?',
        'timestamp': '2025-08-14T10:00:05Z'
    },
    {
        'id': 2,
        'role': 'bot',
        'content': 'No, I am a chatbot. How can I assist you today?',
        'timestamp': '2025-08-14T10:00:10Z'
    },
    {
        'id': 3,
        'role': 'user',
        'content': 'Can you tell me a joke?',
        'timestamp': '2025-08-14T10:01:00Z'
    },
    {
        'id': 4,
        'role': 'bot',
        'content': 'Sure! Why did the scarecrow win an award? Because he was outstanding in his field!',
        'timestamp': '2025-08-14T10:01:05Z'
    }
]

@index_bp.route('/')
def page():
    return render_template('pages/home.html', conversation=conversation)
