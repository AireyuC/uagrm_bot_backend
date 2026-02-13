from django.urls import path
from .views import ChatBotView, SecureUploadView

urlpatterns = [
    path('post/', ChatBotView.as_view(), name='chat_message'),
    path('upload/', SecureUploadView.as_view(), name='secure_upload'),
]
