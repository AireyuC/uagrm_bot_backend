from django.urls import path
from .views import ChatBotView

urlpatterns = [
    path('post/', ChatBotView.as_view(), name='chat_message'),
]
