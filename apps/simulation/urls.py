from django.urls import path
from .views import MockLoginView, MockGradesView, MockDebtView

urlpatterns = [
    path('login/', MockLoginView.as_view(), name='mock_login'),
    path('grades/', MockGradesView.as_view(), name='mock_grades'),
    path('debt/', MockDebtView.as_view(), name='mock_debt'),
]
