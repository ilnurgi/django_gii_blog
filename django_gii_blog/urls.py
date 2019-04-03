from django.urls import path

from django_gii_blog.views import PostsListView, PostDetailView

urlpatterns = [
    path('<int:pk>', PostDetailView.as_view(), name='post-item'),
    path('', PostsListView.as_view(), name='post-list'),
]
