
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('unicorn/', include('django_unicorn.urls')),
    path('admin/', admin.site.urls),
    path('encryption/', include('stegnography.urls')),
    
]
