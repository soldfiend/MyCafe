from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('upload_home_page_photo/', views.upload_home_page_photo, name='upload_home_page_photo'),
    path('delete_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('contact_view', views.contact_view, name='contact_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
