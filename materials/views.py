from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPaginator
from materials.serializers import CourseLessonSerializer, CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseLessonSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            print("три")
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer]
    pagination_class = MaterialsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModer | IsOwner]


class SubscriptionAPIView(APIView):
    """Управление подпиской"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(method="post", auto_schema=None)
    @action(detail=False, methods=["post"])
    def post(self, *args, **kwargs):
        """Включение и отключение подписки"""
        subscriber = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(subscriber=subscriber, course=course_item)

        # Если подписка существует, то получаем её
        if subs_item.exists():
            subs_item = Subscription.objects.get(subscriber=subscriber, course=course_item)
            # изменение существующей подписки
            if subs_item.is_tag:
                subs_item.is_tag = False
                message = "Подписка удалена"
            else:
                subs_item.is_tag = True
                message = "Подписка добавлена"
            subs_item.save()
        # Если подписка НЕ существует, создаем её
        else:
            Subscription.objects.create(subscriber=subscriber, course=course_item, is_tag=True)
            message = "Подписка добавлена"
        return Response({"message": message})
