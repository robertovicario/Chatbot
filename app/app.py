from flask import Flask

from routes.chat import chat_bp
from routes.fallback import fallback_bp
from routes.index import index_bp

# -------------------------

app = Flask(__name__)

# -------------------------

"""
Blueprints Registration
"""
app.register_blueprint(chat_bp)
app.register_blueprint(fallback_bp)
app.register_blueprint(index_bp)

# -------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
