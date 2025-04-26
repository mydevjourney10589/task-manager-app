from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append({'task': task, 'completed': False})
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = True
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if not (0 <= task_id < len(tasks)):
        return redirect('/')  # Redirect if task_id is invalid

    if request.method == 'POST':
        updated_task = request.form.get('updated_task')
        if updated_task:  # Ensure the updated task is not empty
            tasks[task_id]['task'] = updated_task
        return redirect('/')  # Redirect to index after editing or if update is empty
    else: # GET request
        task = tasks[task_id]
        return render_template('edit.html', task=task, task_id=task_id)


if __name__ == '__main__':
    app.run(debug=True)
