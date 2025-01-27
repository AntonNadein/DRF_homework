from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from users.models import ModelUser, Payment
from users.serializers import PaymentSerializer, UserSerializer


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
        """создаем пользователя с защищенным паролем"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UsersDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = ModelUser.objects.all()
    permission_classes = [IsAuthenticated]

    # def get_object(self):
    #     """Получаем текущего аутентифицированного пользователя"""
    #     return self.request.user
