from django.urls import path
from .views import PublicSettingsView, SettingsView
urlpatterns=[path("settings/public/",PublicSettingsView.as_view()),path("settings/",SettingsView.as_view())]
