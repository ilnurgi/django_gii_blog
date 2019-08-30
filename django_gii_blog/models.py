"""
модели блога
"""

import os

from time import time

from django.contrib.auth.models import User
from django.db import models

from markdown import markdown


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

        super().save(*args, **kwargs)


def upload_to(instance, filename):
    """
    вычисляем путь загрузки файла
    """
    return os.path.join(
        'django_gii_blog',
        '{0}_{1}_{2}'.format(instance.post_id, int(time()), filename)
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
