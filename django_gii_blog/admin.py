"""
админки блога
"""

from django.contrib import admin

from django_gii_blog.models import Post


class PostAdmin(admin.ModelAdmin):
    """
    админка сообщений
    """

    list_display = ('title', 'created', 'published')
    fields = (('title', 'created', 'published'), 'short_text', 'text_raw')


admin.site.register(Post, PostAdmin)
