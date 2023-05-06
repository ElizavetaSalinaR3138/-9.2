import flask
import sqlalchemy.sql
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ElizabethSalin:5432@localhost/test'
db = SQLAlchemy(app)


class Note(db.Model):
    note = db.Column(db.String(128), primary_key=True)
    important = db.Column(db.String(128), nullable=False)


@app.route('/', methods=['GET'])
def hello():
    return flask.render_template('index.html', notes=Note.query.all())


@app.route('/add_message', methods=['POST'])
def add_message():
    note = flask.request.form['note']
    important = flask.request.form['important']

    # messages.append(Message(text, tag))
    db.session.add(Note(note=note, important=important))
    db.session.commit()

    return flask.redirect(flask.url_for('hello'))


@app.route('/clear', methods=['POST'])
def clear():
    db.session.execute(sqlalchemy.sql.text("DELETE FROM note"))
    db.session.commit()
    return flask.redirect(flask.url_for('hello'))



with app.app_context():
    db.create_all()
app.run()
