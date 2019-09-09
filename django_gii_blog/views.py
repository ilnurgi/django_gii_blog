"""
представления блога
"""

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import mail_admins
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

        if not self.request.user.is_superuser:
            qs = qs.filter(published=True)

        return qs.order_by('-created')


class PostDetailView(DetailView):
    """
    детализация сообщения
    """
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']

        comments = Comment.objects.filter(post_id=post.id)

        if not self.request.user.is_authenticated:
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
    user_name = request.user.username or request.POST.get('user_name')
    comment = request.POST.get('comment', '').strip()
    post_id = request.POST.get('post_id')

    if all((post_id, user_name, comment, post_id)):
        comment = Comment(comment=comment, user_name=user_name, post_id=post_id)
        if user.is_authenticated:
            comment.user = user
        comment.save()

        messages.add_message(request, messages.INFO, 'Комментарии добавлен, появится после модерации')
        mail_admins(
            'DJANGO_GII_BLOG',
            'blog comment_add\n{post_id}\n{user_name}\n{comment}'.format(
                post_id=post_id,
                comment=comment,
                user_name=user_name
            )
        )
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
