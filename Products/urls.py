from django.urls import path
from . import views
from Products.apis import Get_Product,Get_Product_Image

urlpatterns = [
    path('get_products/',Get_Product.as_view(),name='get_product'),
    path('product/', views.Product_Dashboard, name='product'),       # example.com/
    path("get_product_image/",Get_Product_Image.as_view(),name="get_product_image")
]