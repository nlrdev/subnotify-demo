from django.urls import path
from .views import (
    portal,
)

urlpatterns = [
    path("", portal, name="portal"),
    path("<slug:page>/", portal, name="portal"),
    path("<slug:page>/<slug:function>/", portal, name="portal"),
]
