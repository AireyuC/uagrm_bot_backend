from django.urls import path, include
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="UAGRM Bot API",
      default_version='v1',
      description="Documentación de los endpoints del chatbot",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

from django.contrib.auth.models import Group

try:
    admin.site.unregister(Group)
except Exception:
    pass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', include('apps.chatbot.api.urls')),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/institutional/', include('apps.institutional.urls')),
    path('chat/', include('apps.chatbot.urls')),
    
    # Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # demo path removed
]
