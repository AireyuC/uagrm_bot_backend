from django.urls import path
from .views import LinkStudentView

urlpatterns = [
    path('link/', LinkStudentView.as_view(), name='link_student'),
]
