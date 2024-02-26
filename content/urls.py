from django.urls import re_path

from content.views.content_view import ContentView

urlpatterns = [
    re_path(r'^$', ContentView.as_view()),
]