from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django_gii_blog.models import Post


class PostsListView(ListView):
    model = Post
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
