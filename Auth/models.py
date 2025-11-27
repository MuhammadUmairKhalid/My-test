from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class User(AbstractUser):
    is_verfied = models.BooleanField(default=False)

class OTP(models.Model):
    otp = models.IntegerField(max_length=4)
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField()
    def save(self, *args, **kwargs):
        if not self.expired_at:  # set expiry only when first created
            self.expired_at = timezone.now() + timedelta(minutes=1)  # 1 min expiry
        super().save(*args, **kwargs)
    def is_expired(self):
        return timezone.now() > self.expired_at