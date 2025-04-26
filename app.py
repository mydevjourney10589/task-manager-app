from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Define the Task database model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    all_tasks = Task.query.all()
    return render_template('index.html', tasks=all_tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_description = request.form.get('task') # Renamed variable for clarity
    if task_description:
        new_task = Task(description=task_description)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = True
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id) # Fetch task once for both methods

    if request.method == 'POST':
        updated_description = request.form.get('updated_task')
        if updated_description:  # Only update if the new description is not empty
            task.description = updated_description
            db.session.commit()
        return redirect('/')  # Redirect after POST, regardless of update
    else: # GET request
        # Task is already fetched
        return render_template('edit.html', task=task, task_id=task_id) # Pass task_id for action URL


if __name__ == '__main__':
    app.run(debug=True)
