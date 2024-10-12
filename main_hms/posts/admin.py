from django.contrib import admin
from .models import Posts


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'available', 'created_at')
    list_filter = ("available",)
    search_fields = ['title', 'content']
    ordering = ['-created_at']
    prepopulated_fields = {'slug': ('title',)} 
