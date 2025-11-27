from django.shortcuts import render

# Create your views here.
def Signup_view(request):
    return render(request,"Dashboard/signup.html")

def Login_view(request):
    return render(request,"Dashboard/login.html")

def Otp_View(request):
    return render(request,"Dashboard/otpp.html")

