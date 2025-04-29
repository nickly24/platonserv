from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Пример данных об оценках (улучшено для хранения нескольких оценок по предмету)
student_grades = {
    "Иван": {
        "русский": [4, 5],  # Список оценок по русскому
        "математика": [5],
        "английский": [3, 4, 5]
    },
    "Мария": {
        "русский": [5],
        "математика": [4, 4],
        "английский": [5]
    },
    "Петр": {
        "русский": [3],
        "математика": [3, 3],
        "английский": [4]
    },
}


# Роут для получения всех данных
@app.route("/api", methods=["GET"])
def get_all_grades():
    return jsonify(student_grades)

# Роут для добавления оценки
@app.route("/api/add_grade", methods=["POST"])
def add_grade():
    data = request.get_json()
    student_name = data.get("student_name")
    subject = data.get("subject")
    grade = data.get("grade")

    if not all([student_name, subject, grade]):
        return jsonify({"message": "Необходимы все поля: student_name, subject, grade"}), 400

    try:
        grade = int(grade)
        if not 2 <= grade <= 5:
            return jsonify({"message": "Оценка должна быть от 2 до 5"}), 400
    except ValueError:
        return jsonify({"message": "Оценка должна быть числом"}), 400

    if student_name not in student_grades:
        student_grades[student_name] = {}

    if subject not in student_grades[student_name]:
        student_grades[student_name][subject] = [] # создаем список, если предмета нет

    student_grades[student_name][subject].append(grade) # добавляем оценку в список
    return jsonify({"message": f"Оценка для {student_name} по {subject} добавлена"}), 201

# Роут для удаления оценки (удаляем конкретную оценку)
@app.route("/api/delete_grade", methods=["DELETE"])
def delete_grade():
    data = request.get_json()
    student_name = data.get("student_name")
    subject = data.get("subject")
    grade_index = data.get("grade_index") #индекс удаляемой оценки

    if not all([student_name, subject, grade_index is not None]):
        return jsonify({"message": "Необходимы поля: student_name, subject, grade_index"}), 400

    try:
        grade_index = int(grade_index)
    except ValueError:
        return jsonify({"message": "grade_index должен быть целым числом"}), 400

    if student_name not in student_grades or subject not in student_grades[student_name] or not (0 <= grade_index < len(student_grades[student_name][subject])):
        return jsonify({"message": "Оценка не найдена"}), 404

    del student_grades[student_name][subject][grade_index]  # Удаляем оценку по индексу

    return jsonify({"message": f"Оценка для {student_name} по {subject} с индексом {grade_index} удалена"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80) 