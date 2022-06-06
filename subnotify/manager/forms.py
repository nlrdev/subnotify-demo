from django import forms
from .models import Service, Subscription, Client


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name"]


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["name", "frequency", "sms", "email", "push", "start_date"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["cell", "email"]


class ClientSubForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["subscriptions"]