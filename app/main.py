from datetime import timedelta

from common.configuration import FLASK_SECRET, FLASK_SESSION_LIFETIME
from flask import Flask
from flaskext.markdown import Markdown
from routes import routes
from sassutils.wsgi import SassMiddleware

app = Flask(__name__)

app.secret_key = FLASK_SECRET
app.permanent_session_lifetime = timedelta(minutes=FLASK_SESSION_LIFETIME)

app.wsgi_app = SassMiddleware(
    app.wsgi_app, {__name__: ("static/sass", "static/css", "static/css/")}
)

Markdown(app)

for blueprint, prefix in routes:
    if len(prefix):
        app.register_blueprint(blueprint, url_prefix=prefix)
        continue
    app.register_blueprint(blueprint)
