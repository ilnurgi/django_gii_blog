"""
админки блога
"""

from django.contrib import admin
from django.utils.safestring import mark_safe

from django_gii_blog.models import Post, File, Comment


class FilePostInline(admin.TabularInline):
    """
    связанные с постом файлы
    """
    model = File
    fields = ('field', 'url', 'img')
    readonly_fields = ('url', 'img')
    extra = 1

    def url(self, instance):
        """
        урл до файла
        :param instance:
        :return:
        """
        return instance.field.url

    def img(self, instance):
        return mark_safe('<img src="{}" height=100">'.format(instance.field.url))


class CommentInline(admin.StackedInline):
    """
    связанные сообщения
    """
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    """
    админка сообщений
    """

    list_display = ('title', 'created', 'published')
    fields = (('title', 'created', 'published'), 'short_text', 'text_raw')
    save_on_top = True
    inlines = [
        FilePostInline,
        CommentInline,
    ]


class FileAdmin(admin.ModelAdmin):
    """
    админка файлов сообщений
    """


admin.site.register(Post, PostAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Comment)
