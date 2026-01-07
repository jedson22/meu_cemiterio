from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Sistema de Login/Logout padrão do Django
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', include('core.urls')),
]
