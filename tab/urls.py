from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("teach/", views.teach, name="teach"),
    path("about/", views.about, name="about"),
    path("about/more/", views.more, name="more"),
]