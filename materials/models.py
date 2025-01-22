from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="image/course",
        null=True,
        blank=True,
        verbose_name="Превью курса",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course", null=True, blank=True
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="image/lesson",
        null=True,
        blank=True,
        verbose_name="Превью урока",
    )
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    video_url = models.URLField(max_length=400, null=True, blank=True, verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        "Course", on_delete=models.PROTECT, null=True, blank=True, related_name="lesson", verbose_name="Курс"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson", null=True, blank=True
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
