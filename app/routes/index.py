from flask import Blueprint, render_template

# -------------------------

index_bp = Blueprint('index', __name__)

# -------------------------

conversation = [
    {
        'id': 1,
        'role': 'user',
        'content': 'Ciao!',
        'timestamp': '2025-08-14T10:00:00Z'
    },
    {
        'id': 2,
        'role': 'bot',
        'content': 'Ciao, come stai?',
        'timestamp': '2025-08-14T10:00:05Z'
    }
]

@index_bp.route('/')
def page():
    return render_template('pages/home.html', conversation=conversation)
