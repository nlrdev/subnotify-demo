from django.contrib import admin
from .models import Account, ServiceUser


@admin.register(ServiceUser)
class ServiceUserAdmin(admin.ModelAdmin):
    pass