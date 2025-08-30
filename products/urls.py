from django.urls import path
from . import views 

urlpatterns = [
    path('products/' , views.get_all_products , name='products'),
    path('products/<str:pk>/' , views.get_product_by_id , name='get_product_by_id'),
    path('product/add/' , views.add_product , name='add_product'),
    path('product/update/<str:pk>' , views.update_product , name='update_product'),
    path('product/delete/<str:pk>' , views.delete_product , name='delete_product'),
    path('product/<int:pk>/reviews/', views.create_review , name='create_review'),
    path('product/<int:pk>/reviews/delete/', views.delete_review , name='delete_review'),
]
