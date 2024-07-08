import json
from flask import Flask
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

# Create a Flask application
app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = os.environ.get('USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('PASSWORD')
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://my_user:my_password@postgres/my_database'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'super secret key'
db = SQLAlchemy()

admin = Admin(app)

# Define a model
class SimpleCommand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)

class VerfiedUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    id_username = db.Column(db.Integer, unique=True, nullable=False)
    verify = db.Column(db.Boolean, unique=False, nullable=False)
    room = db.Column(db.Boolean, unique=False, nullable=False)
    plan_id = db.Column(db.Integer, unique=False, nullable=False)
    plan_selected = db.Column(db.Integer, unique=False, nullable=False)
    plan_paid = db.Column(db.Integer, unique=False, nullable=False)


admin.add_view(ModelView(SimpleCommand, db.session))
admin.add_view(ModelView(Config, db.session))
admin.add_view(ModelView(VerfiedUsers, db.session))
db.init_app(app)


@app.route('/simple-commands')
def get_all_users():
    result = db.session.query(SimpleCommand).all()
    if result is not None:
        return json.dumps({
            'result': [{
                'name': simple_command.name,
                'text': simple_command.value,
                'description': simple_command.description
            } for simple_command in result]
        })
    return "No informations yet"


@app.route('/simple-commands/<name>')
def get_users(name):
    result = db.session.query(SimpleCommand).filter_by(name=name).first()
    if result is not None:
        return result.value
    return "No information yet"


@app.route('/configs/<name>')
def get_config(name):
    result = db.session.query(Config).filter_by(name=name).first()
    if result is not None:
        return result.value
    return "No config found"

@app.route('/verified-users')
def get_list_of_verified_users(): #naprawić
    result = db.session.query(VerfiedUsers).all()
    if result is not None:
        return json.dumps({
            'result': [{
                'username': user.username,
                'id_username': user.id_username,
                'verify': user.verify,
                'room': user.room,
                'plan_id': user.plan_id,
                'plan_selected': user.plan_selected,
                'plan_paid': user.plan_paid
            } for user in result]
        })
    return "No informations yet"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


