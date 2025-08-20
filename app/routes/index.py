from datetime import datetime, timezone
from flask import Blueprint, render_template, render_template_string, request, jsonify
from huggingface_hub import InferenceClient
from time import time, sleep
import os

CONVERSATION = []
LLM = InferenceClient(
    provider='groq',
    api_key=os.environ['chatbot'],
)

# -------------------------

index_bp = Blueprint('index', __name__)

# -------------------------

@index_bp.route('/')
def page():
    return render_template('pages/home.html', conversation=CONVERSATION)

@index_bp.route('/chat/user-message', methods=['POST'])
def user_message():
    user_msg = request.json.get('prompt')

    # -------------------------

    CONVERSATION.append({
        'id': len(CONVERSATION) + 1,
        'role': 'user',
        'content': user_msg,
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

    # -------------------------

    user_msg_html = render_template_string(
        "{% import 'includes/message.html' as macros %}{{ macros.message(msg) }}",
        msg=CONVERSATION[-1]
    )

    # -------------------------

    return jsonify({ 'user_msg_html': user_msg_html })

@index_bp.route('/chat/bot-message', methods=['POST'])
def bot_message():

    """
    Clock
    """
    start_time = time()

    # -------------------------

    user_msg = request.json.get('prompt')
    completion = LLM.chat.completions.create(
        model='openai/gpt-oss-20b',
        messages=[
            {
                'role': 'user',
                'content': user_msg
            }
        ],
    )

    # -------------------------

    CONVERSATION.append({
        'id': len(CONVERSATION) + 1,
        'role': 'bot',
        # 'content': f"Your message: {user_msg}",  # FIXME
        'content': completion.choices[0].message.content,
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

    # -------------------------

    bot_msg_html = render_template_string(
        "{% import 'includes/message.html' as macros %}{{ macros.message(msg) }}",
        msg=CONVERSATION[-1]
    )

    # -------------------------

    """
    Clock
    """
    elapsed_time = time() - start_time
    remaining_time = 2 - elapsed_time
    if remaining_time > 0:
        sleep(remaining_time)

    # -------------------------

    return jsonify({ 'bot_msg_html': bot_msg_html })
