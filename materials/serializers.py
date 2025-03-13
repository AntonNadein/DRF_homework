from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Course, Lesson, Subscription
from .validators import VideoURLValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор признака подписки"""

    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса"""

    subscribers = SerializerMethodField(read_only=True)
    # вывод всех существующих записей подписок
    # subscription = SubscriptionSerializer(many=True)

    def get_subscribers(self, instance):
        """Получение списка подписчиков"""
        subscribers = instance.subscription.all()
        subscribers_list = []
        for sub in subscribers:
            if sub.is_tag:
                subscribers_list.append(sub.subscriber.email)
        return subscribers_list
        # вывод всех существующих подписчиков (так же отписавшихся)
        # return [sub.subscriber.email for sub in subscribers]

    class Meta:
        model = Course
        fields = "__all__"
        # fields = (
        #     'id',
        #     'title',
        #     'preview',
        #     'description',
        #     'owner',
        #     'subscription',
        # )


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока"""

    video_url = serializers.URLField(required=False, validators=[VideoURLValidator(field="video_url")])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseLessonSerializer(serializers.ModelSerializer):
    """Сериализатор курса по одному уроку"""

    count_lesson = SerializerMethodField(read_only=True)
    lesson = LessonSerializer(many=True)
    subscribers_user = SerializerMethodField(read_only=True)

    def get_count_lesson(self, instance):
        """Получение количества уроков курса"""
        return instance.lesson.all().count()

    def get_subscribers_user(self, instance):
        """Получение списка подписчиков курса"""
        course_serializer = CourseSerializer(instance)
        return course_serializer.get_subscribers(instance)

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "subscribers_user",
            "count_lesson",
            "lesson",
        )
