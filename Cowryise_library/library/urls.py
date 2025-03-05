from django.urls import path
from .views import *
urlpatterns=[
    path('create-user', RegisterView.as_view()),
    path('all/books', BookView.as_view()),
    path('filter/books', FilterView.as_view()),
    path('book/<int:id>',SpecificView.as_view()),
    path('book',WebHookView.as_view())
]