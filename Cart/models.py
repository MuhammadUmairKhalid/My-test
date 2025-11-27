from django.db import models
from Auth.models import User
from Products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def calculate_total_products_price(self):
        """
        Calculate the total price for all items in this cart.
        """
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def total_price(self):
        """
        Calculate total price for this cart item.
        """
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.name} (x{self.quantity})"
