"""
представления блога
"""

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django_gii_blog.models import Post


class PostsListView(ListView):
    """
    список сообщений
    """
    model = Post
    paginate_by = 10

    def get_queryset(self):
        """
        возвращает qs данных
        """
        qs = super().get_queryset()
        return qs.filter(published=True)


class PostDetailView(DetailView):
    """
    детализация сообщения
    """
    model = Post
