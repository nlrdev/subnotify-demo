from django.contrib import admin
from .models import Manager, Service, Subscription, Client

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass