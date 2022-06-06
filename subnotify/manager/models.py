from django.db import models
from portal.models import ServiceUser
from phonenumber_field.modelfields import PhoneNumberField

class DTModel(models.Model):
    uid = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        ordering = ["created"]

    def activate(self):
        self.active = True
        self.save(update_fields=["active", "updated"])
        
    def deactivate(self):
        self.active = False
        self.save(update_fields=["active", "updated"])
                

class Manager(DTModel):
    user = models.OneToOneField(ServiceUser, related_name="manger", on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Service(DTModel):
    manager = models.ForeignKey(Manager, related_name="services", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subscription(DTModel):
    service = models.ForeignKey(Service, related_name="subscriptions", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)    
    sms = models.BooleanField(default=False)
    email = models.BooleanField(default=False)
    push = models.BooleanField(default=False)    
    start_date = models.DateField(default="0000-00-00")    
    data = models.CharField(max_length=4096)
    class Frequency(models.TextChoices):
        HOUR = "hourly"
        DAY = "daily"
        MONTH = "monthly"
        BIMONTH = "bi-monthly"
        TRIMONTH = "tri-monthly"
        YEAR = "yearly"      
        
    frequency = models.CharField(
        max_length=12,
        choices=Frequency.choices,
        default=Frequency.MONTH,
    )
    
    def __str__(self):
        return self.name


class Client(DTModel):
    manager = models.ForeignKey(Manager, related_name="clients", on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(Subscription)
    cell = PhoneNumberField(blank=True)
    email = models.CharField(max_length=255)
    
    def __str__(self):
        return self.email
