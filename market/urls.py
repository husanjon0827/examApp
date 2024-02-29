# urls.py
from django.urls import path
from .views import HomeView, ProductListView, ProductDetailView, AuthorListView, AuthorDetailView, ProfileView, \
    AuthorLogoutView, CreateProductView, AuthorRegisterView, AuthorLoginView, ProductUpdateView, LikeAuthorView

app_name = 'market'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('explore/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('authors/', AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('create/', CreateProductView.as_view(), name='create_product'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', AuthorLoginView.as_view(), name='login'),
    path('register/', AuthorRegisterView.as_view(), name='register'),
    path('logout/', AuthorLogoutView.as_view(), name='logout'),
    path('like_author/<int:author_id>/', LikeAuthorView.as_view(), name='like_author'),
]