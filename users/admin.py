from django.contrib import admin

from .models import ModelUser, Payment

admin.site.register(ModelUser)
admin.site.register(Payment)
