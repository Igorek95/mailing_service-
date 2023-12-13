from django.contrib import admin

from blog.models import BlogEntry


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('entry_title', 'entry_slug', 'entry_body',
                    'is_published', 'views_count')
