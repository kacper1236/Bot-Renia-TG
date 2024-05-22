import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


# Create a Flask application
app = Flask(__name__)

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


admin.add_view(ModelView(SimpleCommand, db.session))
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
    return "No informations yet"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


