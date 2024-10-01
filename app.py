from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Список задач будет храниться в памяти
todos = []

# Функция для поиска задачи по ID
def find_todo(todo_id):
    return next((todo for todo in todos if todo['id'] == todo_id), None)

# 1. Получение всех задач (Read)
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

# 2. Создание новой задачи (Create)
@app.route('/todos', methods=['POST'])
def create_todo():
    if not request.json or 'title' not in request.json:
        abort(400, description="Bad Request: 'title' is required")
    
    new_todo = {
        'id': len(todos) + 1,  # Простая генерация ID
        'title': request.json['title'],
        'done': False
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

# 3. Обновление статуса задачи (Update)
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = find_todo(todo_id)
    if todo is None:
        abort(404, description="Todo not found")
    
    if not request.json:
        abort(400, description="Bad Request: JSON data is required")
    
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400, description="Bad Request: 'title' must be a string")
    
    if 'done' in request.json and type(request.json['done']) != bool:
        abort(400, description="Bad Request: 'done' must be a boolean")
    
    todo['title'] = request.json.get('title', todo['title'])
    todo['done'] = request.json.get('done', todo['done'])
    
    return jsonify(todo), 200

# 4. Удаление задачи (Delete)
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = find_todo(todo_id)
    if todo is None:
        abort(404, description="Todo not found")
    
    todos.remove(todo)
    return jsonify({'result': True}), 200

if __name__ == '__main__':
    app.run(debug=True)
