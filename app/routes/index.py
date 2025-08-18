from datetime import datetime, timezone
from flask import Blueprint, render_template, render_template_string, request, jsonify
from huggingface_hub import InferenceClient
from time import time, sleep
import os

CONVERSATION = [
    {
        'id': 1,
        'role': 'user',
        'content': 'Hello!',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 2,
        'role': 'bot',
        'content': 'Hi there! How can I help you today?',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 3,
        'role': 'user',
        'content': 'Can you tell me a joke?',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 4,
        'role': 'bot',
        'content': 'Why did the scarecrow win an award? Because he was outstanding in his field!',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 5,
        'role': 'user',
        'content': 'That was funny!',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 6,
        'role': 'bot',
        'content': 'Glad you liked it! Do you want to hear another one?',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 7,
        'role': 'user',
        'content': 'No, thank you. What is the weather like today?',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 8,
        'role': 'bot',
        'content': 'I am not able to check real-time weather, but you can use a weather app for the latest updates.',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 9,
        'role': 'user',
        'content': 'Okay, thanks for your help.',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 10,
        'role': 'bot',
        'content': 'You\'re welcome! If you have more questions, feel free to ask.',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 11,
        'role': 'user',
        'content': 'Can you recommend a good book?',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 12,
        'role': 'bot',
        'content': 'Sure! "To Kill a Mockingbird" by Harper Lee is a classic. Would you like more recommendations?',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 13,
        'role': 'user',
        'content': 'No, that\'s enough for now.',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 14,
        'role': 'bot',
        'content': 'Alright! Let me know if you need anything else.',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'id': 15,
        'role': 'user',
        'content': 'Goodbye!',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
]
LLM = InferenceClient(
    provider='groq',
    api_key=os.environ['HF_TOKEN'],
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
