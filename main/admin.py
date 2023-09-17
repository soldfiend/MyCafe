from django.contrib import admin
from .models import HomePagePhoto


@admin.register(HomePagePhoto)
class HomePagePhotoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image',)
    search_fields = ('caption',)


admin.site.enable_nav_sidebar = False
admin.autodiscover()
