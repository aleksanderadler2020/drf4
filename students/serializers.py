from rest_framework import serializers

from students.models import Course

from django_testing.settings import MAX_STUDENTS_PER_COURSE


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        if len(value) > MAX_STUDENTS_PER_COURSE:
            raise ValueError(f'Максимальное кол-во студентов на курсе {MAX_STUDENTS_PER_COURSE}')

        return value
