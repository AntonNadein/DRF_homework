from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import ModelUser


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = ModelUser.objects.create(email="test@test.ru")
        self.course = Course.objects.create(title="Python", description="Силизерин рулит!", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Python", description="Силизерин рулит!", course=self.course, owner=self.user
        )
        self.group = Group.objects.create(name="moders")
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест получения урока"""
        url = reverse("materials:lesson_get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """Тест создания урока"""
        url = reverse("materials:lesson_create")
        data = {
            "title": "JS",
            "description": "test",
        }
        response = self.client.post(url, data)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        data_2 = {"title": "JS", "description": "test", "video_url": "https://www.youtube.com/"}
        self.client.post(url, data_2)
        self.assertEqual(Lesson.objects.all().count(), 3)

    def test_lesson_create_error(self):
        """Тест валидатора ссылки youtube.com"""
        url = reverse("materials:lesson_create")
        data = {"title": "JS", "description": "test", "video_url": "https://www.youtub.com/"}
        response = self.client.post(url, data)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

    def test_lesson_update(self):
        """Тест обновления урока"""
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"title": "JS"}
        response = self.client.patch(url, data)
        data = response.json()
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "JS")

    def test_lesson_delete(self):
        """Тест удаления урока"""
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест вывода списка уроков"""
        self.user.groups.add(self.group)
        self.user.save()
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        status_code_lesson = response.status_code
        data = response.json()
        self.assertEqual(status_code_lesson, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": None,
                    "title": self.lesson.title,
                    "preview": None,
                    "description": self.lesson.description,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = ModelUser.objects.create(email="test@test.ru")
        self.course = Course.objects.create(title="Js", description="Фронт", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """Тест создания подписки"""
        url = reverse("materials:subscription_post")
        data = {
            "subscriber": self.user.pk,
            "course": self.course.pk,
        }
        # создание подписки в БД
        response = self.client.post(url, data)
        status_code_lesson = response.status_code
        self.assertEqual(status_code_lesson, status.HTTP_200_OK)
        self.assertTrue((Subscription.objects.get(subscriber=self.user.pk, course=self.course.pk).is_tag))
        self.assertEqual(response.json().get("message"), "Подписка добавлена")

        # отключение подписки
        response_2 = self.client.post(url, data)
        status_code_lesson = response_2.status_code
        self.assertEqual(status_code_lesson, status.HTTP_200_OK)
        self.assertFalse((Subscription.objects.get(subscriber=self.user.pk, course=self.course.pk).is_tag))
        self.assertEqual(response_2.json().get("message"), "Подписка удалена")

        # включение подписки
        response_3 = self.client.post(url, data)
        status_code_lesson = response_3.status_code
        self.assertEqual(status_code_lesson, status.HTTP_200_OK)
        self.assertTrue((Subscription.objects.get(subscriber=self.user.pk, course=self.course.pk).is_tag))
        self.assertEqual(response_3.json().get("message"), "Подписка добавлена")
