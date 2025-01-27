from rest_framework import serializers

from .models import ModelUser, Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelUser
        fields = "__all__"
