from django.urls import path
from .api.views import DocumentListCreateView, DocumentVerifyView

urlpatterns = [
    path('documents/', DocumentListCreateView.as_view(), name='document-list-create'),
    path('documents/<int:pk>/verify/', DocumentVerifyView.as_view(), name='document-verify'),
]
