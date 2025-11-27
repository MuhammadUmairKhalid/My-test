from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Product,User
from Cart.serializers import CartItemSerializer, CartSerializer
from rest_framework.permissions import AllowAny

class CartView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    # serializer_class = CartItemSerializer
    # queryset = CartItem.objects.all()

    # ------------------- CREATE -------------------
    def create(self, request, *args, **kwargs):
        """
        Add a product to the user's cart or update quantity if it already exists.
        """
        user_id = 16
        # print("user...",user)
        product_id = request.data.get("product_id")
        print("product_id.......",product_id)
        quantity = int(request.data.get("quantity", 1))

        # Check product exists
        try:
            product = Product.objects.get(stripe_product_id=product_id)
            print("product_id...",product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(id=user_id)
        # Get or create cart for the user
        cart, _ = Cart.objects.get_or_create(user=user)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            # If it already exists, just update quantity
            cart_item.quantity += quantity
            cart_item.save()
            message = "Product quantity updated in cart"
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = "Product added to cart"

        return Response(
            {"message": message, "cart_item": CartItemSerializer(cart_item).data},
            status=status.HTTP_201_CREATED,
        )
    # ------------------- LIST -------------------
    def list(self, request, *args, **kwargs):
        """
        Show all items in the user's cart with total price.
        """
        print("acesss to get api...")
        user = 16
        print(user)
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"message": "Your cart is empty."}, status=status.HTTP_200_OK)

        items = CartItem.objects.all(cart=cart)
        print("items",items)
        serializer = CartItemSerializer(items, many=True)

        total = sum([item.get_total_price() for item in items])

        return Response({
            "user": user.email,
            "cart_items": serializer.data,
            "total_price": total
        })

    # ------------------- UPDATE -------------------
    def update(self, request, *args, **kwargs):
        """
        Update the quantity of a product in the cart.
        """
        user = request.user
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            cart = Cart.objects.get(user=user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Cart item updated", "data": CartItemSerializer(cart_item).data})

    # ------------------- DESTROY -------------------
    def destroy(self, request, *args, **kwargs):
        """
        Remove a product from the cart.
        """
        user = request.user
        product_id = request.data.get("product_id")

        try:
            cart = Cart.objects.get(user=user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"message": "Product removed from cart"}, status=status.HTTP_204_NO_CONTENT)
