from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', cache_page(30)(BlogListView.as_view()), name='blog'),
    path('view/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='view_blog'),
    path('create/', BlogCreateView.as_view(), name='create_blog'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit_blog'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog')

]