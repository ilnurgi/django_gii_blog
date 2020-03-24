"""
модели блога
"""

import os
import re

from time import time

from django.contrib.auth.models import User
from django.db import models

from markdown import markdown
from htmlmin import minify

from gii_django_blog.helpers import cyrillic_to_latin


class Post(models.Model):
    """
    модель сообщения
    """

    title = models.CharField(max_length=255)

    created = models.DateField(auto_created=True)
    updated = models.DateField(auto_now=True)

    text_raw = models.TextField()
    text = models.TextField(blank=True)

    short_text_raw = models.TextField()
    short_text = models.TextField(blank=True)

    published = models.BooleanField(default=False)

    def __str__(self):
        """
        строковое представление объекта
        :return:
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        сохранение модели
        """
        self.short_text = markdown(self.short_text_raw, extensions=['codehilite'])
        self.text = markdown(self.text_raw, extensions=['codehilite'])
        self.text = self.process_tags(self.text)
        self.text = minify(self.text)

        super().save(*args, **kwargs)

    @staticmethod
    def process_tags(text: str) -> text:
        for pattern, repl in (
                (r'<!(div|style|details|summary)(\.)([-\w]+)', r'<\g<1> class="\g<3>">'),
                (r'<!(div|style|details|summary)', r'<\g<1>>'),
                (r'<!/(div|style|details|summary)', r'</\g<1>>'),
        ):
            text = re.sub(pattern, repl, text)
        return text


def upload_to(instance, filename):
    """
    вычисляем путь загрузки файла
    """
    return os.path.join(
        'gii_django_blog',
        '{0}_{1}_{2}'.format(instance.post_id, int(time()), cyrillic_to_latin(filename))
    )


class File(models.Model):
    """
    файлы сообщений
    """

    field = models.FileField(upload_to=upload_to)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        """
        строковое представление объекта
        :return:
        """
        return '{0}/{1}'.format(self.post, self.field.name)

    def delete(self, using=None, keep_parents=False):
        """
        удаление объекта
        :param using:
        :param keep_parents:
        :return:
        """
        super().delete(using=using, keep_parents=keep_parents)

        if os.path.exists(self.field.file.name):
            try:
                os.remove(self.field.file.name)
            except Exception as err:
                pass


class Comment(models.Model):
    """
    коментарии для поста
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=100)
    comment = models.TextField()
    created = models.DateTimeField(auto_created=True, auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    published = models.NullBooleanField()
