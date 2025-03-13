from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentCreateAPIview, PaymentListAPIView, UsersCreateAPIview, UsersDetailAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UsersCreateAPIview.as_view(), name="register"),
    path("<int:pk>/", UsersDetailAPIView.as_view(), name="user_get"),
    path("payment/create/", PaymentCreateAPIview.as_view(), name="payment_create"),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
]
