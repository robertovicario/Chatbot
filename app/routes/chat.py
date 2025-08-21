from datetime import datetime, timezone
from flask import Blueprint, jsonify, render_template_string, request, session
from huggingface_hub import InferenceClient
from time import time, sleep
import os

from routes.utils import init_chat

# -------------------------

MODEL = 'openai/gpt-oss-20b'
LLM = InferenceClient(
    provider='groq',
    api_key=os.environ['HF_TOKEN__Chatbot'],
)

# -------------------------

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

# -------------------------

@chat_bp.route('/user-message', methods=['POST'])
def user_message():

    """
    Session Requirements
    """
    if 'chats' not in session or 'chat_id' not in session or session['chat_id'] not in session['chats']:
        init_chat()

    # -------------------------

    user_msg = request.json.get('prompt')

    # -------------------------

    session['chats'][session['chat_id']]['messages'].append({
        'role': 'user',
        'content': user_msg,
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

    # -------------------------

    user_msg_html = render_template_string(
        "{% import 'includes/message.html' as macros %}{{ macros.message(msg) }}",
        msg=session['chats'][session['chat_id']]['messages'][-1]
    )

    # -------------------------

    return jsonify({ 'user_msg_html': user_msg_html })

@chat_bp.route('/bot-message', methods=['POST'])
def bot_message():

    """
    Clock
    """
    start_time = time()

    # -------------------------

    user_msg = request.json.get('prompt')
    completion = LLM.chat.completions.create(
        model=MODEL,
        messages=[{ 'role': 'user', 'content': user_msg }]
    )

    # -------------------------

    bot_msg = completion.choices[0].message.content
    session['chats'][session['chat_id']]['messages'].append({
        'role': 'bot',
        'content': bot_msg,
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

    # -------------------------

    bot_msg_html = render_template_string(
        "{% import 'includes/message.html' as macros %}{{ macros.message(msg) }}",
        msg=session['chats'][session['chat_id']]['messages'][-1]
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
