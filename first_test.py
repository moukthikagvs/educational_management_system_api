import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
# Test case with valid data
def test_valid_data(client):

    data = {
        "students": [
            {"id": 1, "assignments": [90, 85, 92, 78], "exam": 75},
            {"id": 2, "assignments": [88, 92, 95, 80], "exam": 85}
        ]
    }
    response = client.post('/api/calculate_grades', json=data)  
    result = response.get_json()

    assert response.status_code == 200
    assert len(result['grades']) == 2

  # Test case with invalid data format
def test_invalid_data_format(client):
  
    data = {
        "students": {"id": 1, "assignments": [90, 85, 92, 78], "exam": 75}
    }
    response = client.post('/api/calculate_grades', json=data)  
    result = response.get_json()

    assert response.status_code == 400  
    assert "Invalid format. 'students' must be a list." in result['error']

# Test case with different numbers of assignments and exams
def test_various_assignments_exams(client):

    data = {
        "students": [
            {"id": 1, "assignments": [90, 85], "exam": 75},
            {"id": 2, "assignments": [88, 92, 95, 80, 75], "exam": 85}
        ]
    }
    response = client.post('/api/calculate_grades', json=data)  
    result = response.get_json()

    assert response.status_code == 200
    assert len(result['grades']) == 2


 