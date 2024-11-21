from django.views.decorators.cache import cache_page
from catalog.views import product_detail
from django.urls import path
from .views import ProductListView
from .views import (
    HomepageView, ProductDetailView, ProductCreateView, ProductUpdateView,
    ProductDeleteView, UnpublishProductView, ContactView,
    BlogPostListView, BlogPostDetailView, BlogPostCreateView,
    BlogPostUpdateView, BlogPostDeleteView, VersionCreateView,
    VersionUpdateView, VersionDeleteView, CategoryListView
)

app_name = 'catalog'

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product_list'),
    path('', HomepageView.as_view(), name='homepage'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/new/', ProductCreateView.as_view(), name='create_product'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/unpublish/', UnpublishProductView.as_view(), name='unpublish_product'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('blog/', BlogPostListView.as_view(), name='blogpost_list'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blog/new/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('blog/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('blog/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
    path('version/new/', VersionCreateView.as_view(), name='create_version'),
    path('version/<int:pk>/edit/', VersionUpdateView.as_view(), name='update_version'),
    path('version/<int:pk>/delete/', VersionDeleteView.as_view(), name='delete_version'),
    path('product/<int:pk>/', cache_page(300)(product_detail), name='product_detail'),
    path('product/<int:pk>/', cache_page(60 * 15)(product_detail), name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
]
