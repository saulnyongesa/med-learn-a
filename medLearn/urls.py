
from django.contrib import admin
from medLearn import settings
from django.conf.urls.static import static
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('Home/',include('home.urls') ),
    path('Student/', include('student.urls')),
    path('Author/', include('author.urls')),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
