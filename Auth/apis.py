from rest_framework.views import APIView
from rest_framework.response import Response
from Auth.models import User
from Auth.models import OTP
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from rest_framework import status
from utility import generate_jwt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.views.decorators.csrf import csrf_exempt
import smtplib
import random

def generate_otp() -> str:
    otp = ""
    for _ in range(4):
        otp += str(random.randint(1, 9))
    return otp


def sendEmail(recipient: str, subject: str, body: str):
    sender_email = "umairkhalid1314@gmail.com"
    sender_password = "fbbq kyom achb vngo"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return {'detail': f'Email could not be sent. Error: {str(e)}'}
    

class SignupApi(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")
        print(email,password)
        if User.objects.filter(email=email).first():
            return Response({"message":"User already exist","status":400},status=200)

        if not email or not username or not password:
            return Response({"message": "All fields are required", "status": 400}, status=400)

        # Create User (with password hashing)
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        # Generate OTP
        otp_code = generate_otp()
        otp =OTP.objects.create(user=user, otp=otp_code)
        otp.save()
        # Send Email
        subject = "Your OTP Code"
        body = f"<h3>Your OTP is: {otp_code}</h3>"
        response = sendEmail(recipient=email, subject=subject, body=body)

        if response is True:
            return Response({"message": "OTP has been sent to your email. Please check it.", "status": 200,"user_id":user.id}, status=200)
        else:
            return Response({"message": f"Error while sending the email: {response['detail']}", "status": 400}, status=400)


class Login(APIView):
    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")
        print(email)
        user = User.objects.filter(email=email).first()
        if user:
            db_password = user.password
            is_valid = check_password(password,db_password)
            if is_valid:
                # token = generate_jwt(user=user)
                return Response({"message":"Login Sucessfully","token":"","email":user.email,"status":200})
            else:
                return Response({"message":"Password doesnot match"},status=400)
        else:
            return Response({"message":"Email doesnot Exist"},status=400)

class VerifyOtp(APIView):
    def post(self,request):
        user_id = request.data.get("user_id")
        code = request.data.get("otp")
        print(user_id,code)

        try:
            otp = OTP.objects.filter(user_id=user_id, otp=code).latest("created_at")
        except OTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            print("sff...")
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

        # OTP valid → activate user or mark verified
        return Response({"success": "OTP verified"})


class ResendOtp(APIView):
    def post(request):
        user_id = request.data.get("user_id")
        otp = generate_otp()
        otp = OTP.objects.create(otp= otp)
        otp.save()
        # send_welcome_email()
        return Response(data={"message":"Otp has been resend","status":200})