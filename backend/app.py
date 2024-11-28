import json
from flask import Flask
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import request
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
    is_visible = db.Column(db.Boolean, unique=False, nullable=False)


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)

class VerifiedUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=False, nullable=False)
    id_username = db.Column(db.Integer, unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, unique=False, nullable=False)
    prefered_language = db.Column(db.String(3), unique=False, nullable=False)


admin.add_view(ModelView(SimpleCommand, db.session))
admin.add_view(ModelView(Config, db.session))
admin.add_view(ModelView(VerifiedUsers, db.session))
db.init_app(app)


@app.route('/simple-commands')
def get_all_users():
    result = db.session.query(SimpleCommand).all()
    if result is not None:
        return json.dumps({
            'result': [{
                'name': simple_command.name,
                'text': simple_command.value,
                'description': simple_command.description,
                'is_visible': simple_command.is_visible
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
def get_list_of_verified_users():
    result = db.session.query(VerifiedUsers).all()
    if result is not None:
        return json.dumps({
            'result': [{
                'id': user.id,
                'username': user.username,
                'id_username': user.id_username,
                'is_verified': user.is_verified,
                'prefered_language': user.prefered_language
            } for user in result]
        })
    return "No informations yet"

@app.route('/webhook/unlink-verified-user/<id>', methods=['POST'])
def unlink_verified_user(id):
    data = request.get_json()
    print(data)
    
#dodaj listener z foxonsa

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


