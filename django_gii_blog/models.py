"""
модели блога
"""

import os

from time import time

from django.db import models

from markdown import markdown

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


class Post(models.Model):
    """
    модель сообщения
    """

    title = models.CharField(max_length=255)
    created = models.DateField(auto_created=True)
    updated = models.DateField(auto_now=True)
    text = models.TextField(blank=True)
    text_raw = models.TextField()
    short_text = models.TextField()
    published = models.BooleanField(default=False)

    def __str__(self):
        """
        строковое представление объекта
        :return:
        """
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        сохранение модели
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """

        self.text = self.add_code_style(
            markdown(self.text_raw)
        )

        super(Post, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields)

    def add_code_style(self, content):
        """
        добавялем подсветку кода
        :param content: текст от клиента
        :type content: str
        :rtype: text
        """
        code_start = '<p><code>'
        code_end = '</code></p>'
        code_start_len = len(code_start)
        code_end_len = len(code_end)

        is_code = False
        _lexer = 'text'
        code = []
        result = []

        for line in content.splitlines():
            if line.startswith(code_start):
                is_code = True
                _lexer = line[code_start_len:].strip()
            elif line.endswith(code_end):
                is_code = False
                code.append(line[:-code_end_len])
                try:
                    lexer = get_lexer_by_name(_lexer, stripall=True)
                except ValueError:
                    lexer = get_lexer_by_name('text', stripall=True)
                formatter = HtmlFormatter()
                result.append(
                    highlight(
                        '\n'.join(
                            i.replace('&lt;', '<').replace('&gt;', '>')
                            for i in code),
                        lexer,
                        formatter))
                code = []
                _lexer = 'text'
            elif is_code:
                code.append(line)
            else:
                result.append(line)

        return '\n'.join(result)


def upload_to(instance, filename):
    """
    вычисляем путь загрузки файла
    """
    return os.path.join(
        'django_gii_blog',
        '{0}_{1}{2}'.format(instance.post_id, int(time()), os.path.splitext(filename)[-1])
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
