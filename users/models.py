from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class ModelUser(AbstractUser):
    """Модель пользователь"""

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Модель платеж"""

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(ModelUser, on_delete=models.CASCADE, related_name="payments", verbose_name="Пользователь")
    payment_date = models.DateField(verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="payments", null=True, blank=True, verbose_name="Курс"
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="payments", null=True, blank=True, verbose_name="Урок"
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")
    link = models.URLField(max_length=400, blank=True, null=True, verbose_name="Ссылка на оплату")
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID сессии")

    def __str__(self):
        return f"Платеж {self.id} от {self.user.username} на сумму {self.amount}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "Платежи"
