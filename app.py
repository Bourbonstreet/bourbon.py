from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    important = db.Column(db.Boolean, default=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'clear_notes' in request.form:
            Note.query.delete()
            db.session.commit()
            return redirect(url_for('index'))

        note_text = request.form['note_text']
        is_important = 'note_important' in request.form
        new_note = Note(text=note_text, important=is_important)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('index'))

    notes = Note.query.all()
    return render_template('index.html', notes=notes)


@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    note_to_delete = Note.query.get_or_404(note_id)
    db.session.delete(note_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)