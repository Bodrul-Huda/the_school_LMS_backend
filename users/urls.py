
from django.urls import path

from .views import logout_view, user_list_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/', user_list_view, name='user_list_view'),
    path('auth/logout/', logout_view, name='logout'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)