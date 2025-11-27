import stripe
from rest_framework import request
from rest_framework.response import Response
from Products.models import Product
import requests
from django.http import HttpResponse
from rest_framework.views import APIView
import cv2
import numpy as np

def Resize_Images(image_bytes,width=200,height=200):
    # Convert byte stream to NumPy array
    image_array = np.frombuffer(image_bytes, np.uint8)

    # Decode image
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode image")

    # Resize image
    resized_img = cv2.resize(img, (width, height))

    # Encode back to bytes (JPEG)
    success, buffer = cv2.imencode('.jpg', resized_img)
    if not success:
        raise ValueError("Failed to encode image")

    return buffer.tobytes()


class Get_Product(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        name = data.get('name')
        description = data.get('description')
        image = request.FILES.get('file')  # fixed here
        print(image)
        # print("amount",request.form.get('amount'))
        amount = int(float(data.get('amount')) * 100)  # convert to cents
        stripe.api_key = ""
        print(amount)
        currency = 'usd'  # or your desired currency

        # Upload image to Stripe File object (optional)
        image_upload = stripe.File.create(
            file=image,
            purpose='product_image',
        )

        # Create product with image
        product = stripe.Product.create(
            name=name,
            description=description,
            images=[image_upload['url']]
        )
        
        # Create one-time price
        price = stripe.Price.create(
            unit_amount=amount,
            currency=currency,
            product=product.id
        )
        product = Product(stripe_product_id = product.id ,user_id =17, price = amount , description = description , interval = "one off" , image = image_upload['url'],name=name)
        product.save()
        return HttpResponse({"message":"Products Add Sucessfully"})
    
    def get(self,request,*args,**kwargs):
        products_list = []
        stripe.api_key = "" 
        products = stripe.Product.list()

        for product in products.auto_paging_iter():
            prices = stripe.Price.list(product=product.id)
        
            if prices.data:
                price_obj = prices.data[0]  # Take the first price (or loop if you want all)
                unit_amount = price_obj.unit_amount  # in cents
                currency = price_obj.currency

                # Convert cents to dollars (if needed)
                amount = unit_amount / 100
                product_info = {
                    'name': product.name,
                    'description': product.description,
                    'price': amount,  # note: this is a price ID, not the amount!
                    'status': product.active,
                    'id' : product.id
                }
                products_list.append(product_info)
        print(products_list)

        return Response(products_list)


class Get_Product_Image(APIView):
    def get(self,request,*args,**kwargs):
        prod_id = request.query_params.get("prod_id")
        product = stripe.Product.retrieve(prod_id)
        image_url = product["images"]
        headers = {
        'Authorization': f''    }
        response = requests.get(image_url[0], headers=headers)

        if response.status_code == 200:
            # Call the helper function to resize image
            # resized_bytes = Resize_Images(response.content)
            return HttpResponse(response.content,content_type="image/jpeg")
        else:
            return {"error": "Unable to fetch image"}, 500