from django.urls import path
from .views import *
urlpatterns=[
    path('add', CreateView.as_view()),
    path('delete/<int:id>', DeleteView.as_view()),
    path('users', UsersView.as_view()),
    path('debtors', DebtorsView.as_view()),
    path('unavailable', UnavView.as_view())
]