from flask import Blueprint, render_template

from routes.utils import init_chat

# -------------------------

index_bp = Blueprint('index', __name__)

# -------------------------

@index_bp.route('/')
def page():

    """
    Session Initialization
    """
    init_chat()

    # -------------------------

    return render_template('pages/chat.html')
