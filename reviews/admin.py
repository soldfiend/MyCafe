from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish', 'rating', 'created_at')
    list_filter = ('dish', 'created_at')
    search_fields = ('user__username', 'dish__name')
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

    delete_selected.short_description = "Удалить выбранные отзывы"
