from django.urls import path
from . import views
from Auth.apis import SignupApi,Login,VerifyOtp

urlpatterns = [
    path('signup/', views.Signup_view, name='signup'),       # example.com/
    path('loginn/', views.Login_view, name='loginn'),
    path('otp_page/', views.Otp_View, name='otp_page'),  # example.com/about/
    path("register/", SignupApi.as_view(), name="register"),
    path("check_login/",Login.as_view(),name="login"),
    path("verify_otp/",VerifyOtp.as_view(),name="verify_otp")
]
