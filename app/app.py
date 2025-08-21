from flask import Flask, jsonify, session
from flask_session import Session
import secrets

from routes.chat import chat_bp
from routes.fallback import fallback_bp
from routes.index import index_bp

# -------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

"""
Blueprints Registration
"""
app.register_blueprint(chat_bp)
app.register_blueprint(fallback_bp)
app.register_blueprint(index_bp)

# -------------------------

@app.route('/session')
def app_session():
    return jsonify(dict(session))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
