from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import (BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView,
                        status_published)

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('detail/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='blog_detail'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('published/<int:pk>/', status_published, name='status_published'),
]
