from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from users.models import ModelUser, Payment
from users.serializers import PaymentSerializer, UserSerializer
from users.servicies import create_stripe_price, create_stripe_product, create_stripe_session


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)


class UsersCreateAPIview(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = ModelUser.objects.all()

    def perform_create(self, serializer):
        """Создаем пользователя с защищенным паролем"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UsersDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = ModelUser.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIview(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Оплата курса"""
        payment = serializer.save(user=self.request.user)
        if payment.payment_method == "transfer":
            if payment.paid_course:
                name = payment.paid_course.title
            elif payment.paid_lesson:
                name = payment.paid_lesson.title
            else:
                name = "Помощь школе"
            product = create_stripe_product(name)
            amount = create_stripe_price(payment.amount, product)
            session_id, session_link = create_stripe_session(amount)
            payment.session_id = session_id
            payment.link = session_link
            payment.save()
