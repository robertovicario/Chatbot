from datetime import datetime, timezone
from flask import session

def init_chat(chat_id=None):
    """
    Initialize a chat in the Flask session.

    Parameters:
        - chat_id (int): The ID of the chat to initialize. Default is None.
    """

    if 'chats' not in session:
        session['chats'] = {}

    if chat_id is None:
        chat_id = len(session['chats']) + 1

    session['chat_id'] = str(chat_id)
    chat_id_str = session['chat_id']

    if chat_id_str not in session['chats']:
        session['chats'][chat_id_str] = {
            'id': chat_id_str,
            'title': f"Chat {chat_id_str}",
            'messages': []
        }

    session.modified = True

def add_message(role, content, chat_id=None):
    """
    Add a message to the chat.

    Parameters:
        - role (str): The role of the message sender ('user' or 'bot').
        - content (str): The content of the message.
        - chat_id (int): The ID of the chat to initialize. Default is None.
    """

    if chat_id is None:
        chat_id = session.get('chat_id', 1)

    # -------------------------

    init_chat(chat_id)
    session['chats'][chat_id]['messages'].append({
        'role': role,
        'content': content,
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

    session.modified = True
