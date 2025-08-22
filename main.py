from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {'id': 1, 'title': 'Sign up for Replit', 'done': True},
    {'id': 2, 'title': 'Build a REST API', 'done': False}
]

@app.route('/')
def home():
    return jsonify({'message': 'Task API is running!', 'tasks': tasks})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'task': task})

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        return jsonify({'error': 'Missing title in request'}), 400
    new_task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,
        'title': request.json['title'],
        'done': False
    }
    tasks.append(new_task)
    return jsonify({'task': new_task}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'done' in request.json:
        task['done'] = request.json['done']
    return jsonify({'task': task})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task_to_delete = next((task for task in tasks if task['id'] == task_id), None)
    if task_to_delete is None:
        return jsonify({'error': 'Task not found'}), 404
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'result': True})

# This line makes it run on Replit
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
    