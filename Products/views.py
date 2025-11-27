from django.shortcuts import render

# Create your views here.
def Product_Dashboard(request):
    return render(request,"Dashboard/product_dashboard.html")
