from django.urls import path, include

from django_gii_blog.views import index

urlpatterns = [
    path('', index)
]
