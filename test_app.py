import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_todo(client):
    # Тестирование создания новой задачи
    response = client.post('/todos', json={'title': 'Test ToDo'})
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['title'] == 'Test ToDo'
    assert json_data['done'] is False

def test_get_todos(client):
    # Тестирование получения списка задач
    client.post('/todos', json={'title': 'Test ToDo 1'})
    client.post('/todos', json={'title': 'Test ToDo 2'})
    
    response = client.get('/todos')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2

def test_update_todo(client):
    # Тестирование обновления задачи
    client.post('/todos', json={'title': 'Test ToDo'})
    
    response = client.put('/todos/1', json={'title': 'Updated ToDo', 'done': True})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['title'] == 'Updated ToDo'
    assert json_data['done'] is True

def test_delete_todo(client):
    # Тестирование удаления задачи
    client.post('/todos', json={'title': 'Test ToDo'})
    
    response = client.delete('/todos/1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['result'] is True

    # Проверка, что задача была удалена
    response = client.get('/todos')
    json_data = response.get_json()
    assert len(json_data) == 0
