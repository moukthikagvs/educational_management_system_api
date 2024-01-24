from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_finalgrades(assignments_score, exam_score):
    assignments_weight = 0.6
    exam_weight = 0.4

    if all(0 <= score <= 100 for score in assignments_score) and 0 <= exam_score <= 100:
        final_grade = assignments_weight * (sum(assignments_score) / len(assignments_score)) + exam_weight * exam_score
        return round(final_grade, 1)
    else:
        raise ValueError("Invalid score. Scores must be between 0 and 100.")

@app.route('/api/calculate_grades', methods=['POST'])
def calculate_grades():
    data = request.get_json()
    students = data.get('students', [])

    if not isinstance(students, list):
        return jsonify({"error": "Invalid format. 'students' must be a list."}), 400

    result = []
    for student in students:
        student_id = student.get('id')
        assignments = student.get('assignments', [])
        exam = student.get('exam')
        if not isinstance(student_id, int) or not isinstance(assignments, list) or not isinstance(exam, int):
            return jsonify({"error": "Invalid format ."}), 400

        final_grade = calculate_finalgrades(assignments, exam)

        result_item = f'{{"id": {student_id}, "finalGrade": {final_grade}}}'
        result.append(result_item)

    response_data = f'{{"grades": [{", ".join(result)}]}}'

    response = app.response_class(
        response=response_data,
        status=200,
        mimetype='application/json'
    )

    return response

if __name__ == "__main__":
    app.run(debug=True)
