from flask import Flask, jsonify, request
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)  # Разрешает запросы с любых доменов

# Используем список для хранения студентов
# students = [
#    {"id": 1, "name": "Иван Иванов", "group": "ПИ-101"},
#    {"id": 2, "name": "Мария Петрова", "group": "ИС-202"}
# ]
students = [
    {'id': 1, 'name': 'Анжелика Станиславовна Гаврилова', 'group': 'ПИ-101', 'email': 'adam_71@example.com'},
    {'id': 2, 'name': 'Ермолай Фокич Медведев', 'group': 'ВТ-505', 'email': 'foka_03@example.net'},
    {'id': 3, 'name': 'Лаврентий Иларионович Фадеев', 'group': 'ВТ-505', 'email': 'qmironov@example.net'},
    {'id': 4, 'name': 'Гришина Евпраксия Макаровна', 'group': 'ПИ-101', 'email': 'fprohorov@example.org'},
    {'id': 5, 'name': 'Гуляева Ульяна Федоровна', 'group': 'ПИ-101', 'email': 'filatovipat@example.org'},
    {'id': 6, 'name': 'Симон Антипович Иванов', 'group': 'ИТ-404', 'email': 'timofeevavera@example.net'},
    {'id': 7, 'name': 'Белова Милица Яковлевна', 'group': 'ПИ-101', 'email': 'oktjabrinagureva@example.com'},
    {'id': 8, 'name': 'Анна Николаевна Калашникова', 'group': 'ПИ-101', 'email': 'leonti82@example.net'},
    {'id': 9, 'name': 'Князева Фаина Владимировна', 'group': 'ИС-202', 'email': 'leon_20@example.com'},
    {'id': 10, 'name': 'Зинаида Богдановна Рожкова', 'group': 'ИС-202', 'email': 'julian_1977@example.org'},
    {'id': 8, 'name': 'Анна Николаевна Калашникова', 'group': 'ПИ-101', 'email': 'leonti82@example.net'},
    {'id': 9, 'name': 'Князева Фаина Владимировна', 'group': 'ИС-202', 'email': 'leon_20@example.com'},
    {'id': 8, 'name': 'Анна Николаевна Калашникова', 'group': 'ПИ-101', 'email': 'leonti82@example.net'},
    {'id': 9, 'name': 'Князева Фаина Владимировна', 'group': 'ИС-202', 'email': 'leon_20@example.com'},
    {'id': 10, 'name': 'Зинаида Богдановна Рожкова', 'group': 'ИС-202', 'email': 'julian_1977@example.org'},
    {'id': 11, 'name': 'Игнатий Гурьевич Королев', 'group': 'ВТ-505', 'email': 'solomonprohorov@example.com'},
    {'id': 12, 'name': 'Беспалов Арефий Тихонович', 'group': 'ИТ-404', 'email': 'agafjabelozerova@example.org'},
    {'id': 13, 'name': 'Радован Викентьевич Козлов', 'group': 'ПИ-101', 'email': 'anisimgromov@example.org'},
    {'id': 14, 'name': 'Прохоров Лучезар Викторович', 'group': 'ИТ-404', 'email': 'alevtina_65@example.net'},
    {'id': 15, 'name': 'Полина Васильевна Калинина', 'group': 'ИТ-404', 'email': 'marija2025@example.net'},
    {'id': 16, 'name': 'Наина Филипповна Назарова', 'group': 'ИТ-404', 'email': 'efremfedotov@example.com'},
    {'id': 17, 'name': 'Артемьева Варвара Святославовна', 'group': 'ВТ-505', 'email': 'kuzma_1983@example.org'},
    {'id': 18, 'name': 'Феврония Никифоровна Горбунова', 'group': 'ИТ-404', 'email': 'jsamsonova@example.net'},
    {'id': 19, 'name': 'Иванов Соломон Харлампович', 'group': 'ПИ-101', 'email': 'nsemenov@example.org'},
    {'id': 20, 'name': 'Любовь Тарасовна Евсеева', 'group': 'ВТ-505', 'email': 'zhanna1979@example.com'},
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

# @app.route('/students', methods=['GET'])
# def get_students():
#     return jsonify({
#         "count": len(students),
#         "students": students
#     })

@app.route('/students', methods=['GET'])
def get_students():
    group_filter = request.args.get('group')
    if group_filter:
        # Фильтруем список по группе
        filtered = [s for s in students if s.get('group') == group_filter]
        return jsonify({
            "count": len(filtered),
            "students": filtered,
            "filter": {"group": group_filter}
        })
    else:
        return jsonify({
        "count": len(students),
        "students": students
    })

# ЭНДПОИНТ ДЛЯ ДОБАВЛЕНИЯ
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

# ЭНДПОИНТ ДЛЯ УДАЛЕНИЯ
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

# ЭНДПОИНТ ДЛЯ РЕДАКТИРОВАНИЯ
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Ищем студента по ID
    for i, student in enumerate(students):
        if student['id'] == student_id:
            # Обновляем поля (если они переданы в запросе)
            if 'name' in data:
                student['name'] = data['name']
            if 'group' in data:
                student['group'] = data['group']
            # Можно также добавить обновление даты, если нужно
            # student['updated'] = datetime.now().isoformat()
            
            return jsonify({
                "message": "Студент обновлён",
                "student": student
            }), 200
    
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
