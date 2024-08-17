
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    # path('unicorn/', include('django_unicorn.urls')),
    path('admin/', admin.site.urls),
    path('encryption/', include('stegnography.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
