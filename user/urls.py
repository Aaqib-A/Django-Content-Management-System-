from django.urls import re_path

from user.views.user_view import UserView

urlpatterns = [
    re_path(r'^$', UserView.as_view()),
]