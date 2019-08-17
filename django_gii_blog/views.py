"""
представления блога
"""

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django_gii_blog.models import Post, Comment


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']

        comments = Comment.objects.filter(post_id=post.id)

        if not self.request.user:
            comments = comments.filter(published=True)
        else:
            user_name = self.request.user.username
            context['user_name'] = user_name

        context['comments'] = comments.order_by('-created')

        return context


def add_comment(request):
    """
    добавляем коментарии к посту
    """
    user = request.user
    user_name = request.user.username or request.POST['user_name']
    comment = request.POST['comment'].strip()
    post_id = request.POST['post_id']

    if all((post_id, user_name, comment, post_id)):
        Comment(user=user, comment=comment, user_name=user_name, post_id=post_id).save()
        messages.add_message(request, messages.INFO, 'Комментарии добавлен, появится после модерации')
    else:
        if not post_id:
            messages.add_message(request, messages.ERROR, 'Не задан идентификатор поста')

        if not user_name:
            messages.add_message(request, messages.ERROR, 'Не задано имя')

        if not comment:
            messages.add_message(request, messages.ERROR, 'Пустой комментарии')

        if not post_id:
            messages.add_message(request, messages.ERROR, 'Не указан пост')

    return redirect(reverse('blog:post-detail', kwargs={'pk': post_id}))
