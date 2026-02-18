from flask import Flask, jsonify, request
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)  # Разрешает запросы с любых доменов

# Используем список для хранения студентов
students = [
    {"id": 1, "name": "Иван Иванов", "group": "ПИ-101"},
    {"id": 2, "name": "Мария Петрова", "group": "ИС-202"}
]

# Получаем ключ из переменных окружения
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    print("⚠️ ВНИМАНИЕ: API_KEY не установлен в переменных окружения!")
    print("Установите API_KEY в Render Dashboard → Environment Variables")
    API_KEY = "default_key_for_dev"  # только для локальной разработки

# Защита API
@app.before_request
def check_api_key():
    # Разрешаем GET запросы без ключа (для фронтенда)
    if request.method == 'GET':
        return
    
    # Для POST/DELETE проверяем ключ
    if request.method in ['POST', 'DELETE', 'PUT']:
        provided_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        # if not API_KEY:
            # return jsonify({"error": "API key not configured on server"}), 500
        
        if API_KEY == "default_key_for_dev":
            return
            
        if provided_key != API_KEY:
            print(f"❌ Неверный ключ! Ожидался: {API_KEY[:5]}..., получен: {provided_key}")
            return jsonify({
                "error": "Invalid API key",
                "message": "Provide valid X-API-Key header"
            }), 403

@app.route('/')
def home():
    return jsonify({
        "message": "🎓 Student API работает!",
        "endpoints": {
            "GET /students": "Все студенты",
            "POST /students": "Добавить студента",
            "DELETE /students/<id>": "Удалить студента",
            "GET /health": "Проверка работы"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({
        "count": len(students),
        "students": students
    })

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Нужно поле 'name'"}), 400
    
    # Находим максимальный ID
    max_id = max([s['id'] for s in students]) if students else 0
    
    student = {
        "id": max_id + 1,
        "name": data['name'],
        "group": data.get('group', 'Не указана'),
        "created": datetime.now().isoformat()
    }
    
    students.append(student) 
    return jsonify(student), 201

# ДОБАВЬТЕ ЭТОТ ЭНДПОИНТ ДЛЯ УДАЛЕНИЯ!
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    # Ищем студента по ID
    for i, student in enumerate(students):
        if student['id'] == student_id:
            deleted = students.pop(i)
            return jsonify({
                "message": "Студент удален",
                "student": deleted
            })
    
    return jsonify({"error": "Студент не найден"}), 404

@app.route('/health')
def health():
    return jsonify({
        "status": "✅ OK",
        "service": "Student API",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
