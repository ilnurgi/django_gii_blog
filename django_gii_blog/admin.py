"""
админки блога
"""

from django.contrib import admin

from django_gii_blog.models import Post, File


class FilePostInline(admin.TabularInline):
    """
    связанные с постом файлы
    """
    model = File
    fields = ('field', 'url')
    readonly_fields = ('url', )

    def url(self, instance):
        """
        урл до файла
        :param instance:
        :return:
        """
        return instance.field.url


class PostAdmin(admin.ModelAdmin):
    """
    админка сообщений
    """

    list_display = ('title', 'created', 'published')
    fields = (('title', 'created', 'published'), 'short_text', 'text_raw')
    inlines = [
        FilePostInline,
    ]


class FileAdmin(admin.ModelAdmin):
    """
    админка файлов сообщений
    """


admin.site.register(Post, PostAdmin)
admin.site.register(File, FileAdmin)
