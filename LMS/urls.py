
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('adminapp.urls')),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),
    path('guest/',include('guest.urls')),
    path('parent/',include('parent.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)