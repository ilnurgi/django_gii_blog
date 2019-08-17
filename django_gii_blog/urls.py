"""
роутинг
"""

from django.urls import path

from django_gii_blog.views import PostsListView, PostDetailView, add_comment

app_name = 'blog'
urlpatterns = [
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('add_comment', add_comment, name='post-add-comment'),
    path('', PostsListView.as_view(), name='post-list'),
]
