from flask import Flask, json, session, render_template, redirect, url_for
from mongoengine import connect
from flask_cors import *
import config
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

app = Flask('digest', static_folder='./static', template_folder='./templates')
app.config.from_object(config)
app.json_encoder = DecimalEncoder
CORS(app, supports_credentials=True)

def register_blueprints():
    from applications.users import user
    from applications.courses import course
    for blueprint in (user, course):
        app.register_blueprint(blueprint)

register_blueprints()

@app.route('/')
def index():
    if 'id' in session:
        return redirect(url_for('course.course_series'))
    return redirect(url_for('user.user_login'))