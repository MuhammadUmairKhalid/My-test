from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Cart.apis import CartView  # import your viewset

# Create a router
router = DefaultRouter()

# Register your ViewSet with the router
router.register(r'cart', CartView, basename='cart')

urlpatterns = [
    path('', include(router.urls)),  # include all the router URLs
]
