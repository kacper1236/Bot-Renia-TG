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


# Create an instance of SQLAlchemy


# Define a model
class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)


admin.add_view(ModelView(Config, db.session))

# Create the database tables
# app = Flask(__name__)
# db.create_all()
# admin = Admin(app, name='microblog', template_mode='bootstrap3')
# admin.add_view(ModelView(Config, db.session))

# Run the Flask application
# if __name__ == '__main__':
#     app.run(debug=True)
db.init_app(app)

with app.app_context():
    db.create_all()
    # howMuchTimeToConvention = Config(name='ile_do_futrolajek', value='621', description='ile dni jest do futrołajek')
    # conventionDate = Config(name='data', value='6.2.1', description='ważne daty')
    # discordLink = Config(name='discord', value='abc', description='link do discorda')
    # websiteLink = Config(name='website', value='def', description='link do strony')
    # db.session.add(howMuchTimeToConvention)
    # db.session.add(conventionDate)
    # db.session.add(discordLink)
    # db.session.add(websiteLink)
    # db.session.commit()

@app.route('/configs')
def get_all_users():
    result = db.session.query(Config).all()
    if result is not None:
        return json.dumps({
            'result': [{
                'name': config.name,
                'text': config.value,
                'description': config.description
            } for config in result]
        })
    return "No informations yet"

@app.route('/config/<name>')
def get_users(name):
    result = db.session.query(Config).filter_by(name=name).first()
    if result is not None:
        return result.value
    return "No informations yet"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


