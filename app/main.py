import asyncio
from datetime import timedelta

from common.configuration import FLASK_SECRET, FLASK_SESSION_LIFETIME
from flask import Flask
from flaskext.markdown import Markdown
from models.user import create_default_admin
from models.page import create_default_pages
from routes import routes
from sassutils.wsgi import SassMiddleware

app = Flask(__name__)

app.secret_key = FLASK_SECRET
app.permanent_session_lifetime = timedelta(minutes=FLASK_SESSION_LIFETIME)

app.wsgi_app = SassMiddleware(
    app.wsgi_app, {__name__: ("static/sass", "static/css", "static/css/", False)}
)

Markdown(app)

for blueprint, prefix in routes:
    if len(prefix):
        app.register_blueprint(blueprint, url_prefix=prefix)
        continue
    app.register_blueprint(blueprint)

asyncio.run(create_default_admin())
asyncio.run(create_default_pages())

if __name__ == "__main__":
    # Run development server
    app.run(host="0.0.0.0", port=8000, debug=True)
