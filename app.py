from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_tools.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models for Syllabus Planner and To-Do List
class Syllabus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Pending')

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Incomplete')

# Home Route
@app.route('/')
def index():
    syllabus = Syllabus.query.all()
    todos = ToDo.query.all()
    return render_template('index.html', syllabus=syllabus, todos=todos)

# Syllabus Management Routes
@app.route('/add_syllabus', methods=['POST'])
def add_syllabus():
    subject = request.form['subject']
    topic = request.form['topic']
    new_entry = Syllabus(subject=subject, topic=topic)
    db.session.add(new_entry)
    db.session.commit()
    flash("Syllabus Entry Added!")
    return redirect(url_for('index'))

@app.route('/update_syllabus/<int:id>')
def update_syllabus(id):
    entry = Syllabus.query.get_or_404(id)
    entry.status = "Completed"
    db.session.commit()
    flash("Syllabus Marked as Completed!")
    return redirect(url_for('index'))

@app.route('/delete_syllabus/<int:id>')
def delete_syllabus(id):
    entry = Syllabus.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash("Syllabus Entry Deleted!")
    return redirect(url_for('index'))

# To-Do List Routes
@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    new_task = ToDo(task=task)
    db.session.add(new_task)
    db.session.commit()
    flash("Task Added!")
    return redirect(url_for('index'))

@app.route('/update_task/<int:id>')
def update_task(id):
    task = ToDo.query.get_or_404(id)
    task.status = "Complete"
    db.session.commit()
    flash("Task Marked as Complete!")
    return redirect(url_for('index'))

@app.route('/delete_task/<int:id>')
def delete_task(id):
    task = ToDo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Task Deleted!")
    return redirect(url_for('index'))

# Educational Tools Routes
@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        expression = request.form['expression']
        result = eval(expression)
        return jsonify({"result": result})
    except Exception:
        return jsonify({"result": "Error in expression"})

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form['text']
    blob = TextBlob(text)
    summary = " ".join(blob.sentences[:2])  # Simple summarization logic
    return jsonify({"summary": summary})

# Run the App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)


