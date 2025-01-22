from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseLessonSerializer(serializers.ModelSerializer):
    count_lesson = SerializerMethodField(read_only=True)
    lesson = LessonSerializer(many=True)

    def get_count_lesson(self, instance):
        return instance.lesson.all().count()

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "count_lesson",
            "lesson",
        )
