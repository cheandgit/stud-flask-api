from flask import Flask, jsonify, request
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

# Для Flask 3.0+
app.json.ensure_ascii = False  # РАБОТАЕТ!

CORS(app)   # Разрешает запросы с любых доменов

# Отключаем ASCII-кодирование для JSON
# app.config['JSON_AS_ASCII'] = False

# Простая "база данных" в памяти
students = {
    1: {"id": 1, "name": "Иван Иванов", "group": "ПИ-101"},
    2: {"id": 2, "name": "Мария Петрова", "group": "ИС-202"}
}

@app.route('/')
def home():
    return jsonify({
        "message": "🎓 Student API работает!",
        "endpoints": {
            "GET /students": "Все студенты",
            "POST /students": "Добавить студента",
            "GET /health": "Проверка работы"
        },
        "deployed_on": "Render + GitHub Codespaces",
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
    
    student = {
        "id": len(students) + 1,
        "name": data['name'],
        "group": data.get('group', 'Не указана'),
        "created": datetime.now().isoformat(),
        # Добавляем инфо о среде
        "deployed_on": "Render" if os.getenv('RENDER') else "Codespaces"
    }
    
    students.append(student)
    return jsonify(student), 201

@app.route('/health')
def health():
    return jsonify({
        "status": "✅ OK",
        "service": "Student API",
        "environment": "Render" if os.getenv('RENDER') else "GitHub Codespaces",
        "timestamp": datetime.now().isoformat()
    })

# Для Render!
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
