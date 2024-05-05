import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course

from django_testing.settings import MAX_STUDENTS_PER_COURSE


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user('admin')


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_first_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)

    # Act
    response = client.get('/api/v1/courses/1/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1 and data['name'] == courses[0].name


@pytest.mark.django_db
def test_get_all_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_get_filter_id_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get(f'/api/v1/courses/?id={str(courses[4].id)}')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[4].id


@pytest.mark.django_db
def test_get_filter_name_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get(f'/api/v1/courses/?name={str(courses[5].name)}')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[5].name


@pytest.mark.django_db
def test_create_courses(client):
    # Arrange
    course = {
        "name": "NewCourse",
        "students": []
    }

    # Act
    response = client.post('/api/v1/courses/', course)
    # Assert
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_courses(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)
    update_course = {
        "name": "NewCourse",
        "students": []
    }
    # Act
    response = client.patch(f'/api/v1/courses/{str(course[0].id)}/', update_course)
    # Assert
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_courses(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)
    # Act
    response = client.delete(f'/api/v1/courses/{str(course[0].id)}/')
    # Assert
    assert response.status_code == 204


#Не очень понял суть доп.задания, если не надо создавать студентов,
# то просто проверить значение переменной MAX_STUDENTS_PER_COURSE?
@pytest.mark.parametrize("test_input,expected", [(19, True), (20, True), (21, False)])
def test_eval(test_input, expected):
    assert (test_input <= MAX_STUDENTS_PER_COURSE) == expected



