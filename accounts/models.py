from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    ip_address = models.GenericIPAddressField()
    session = models.CharField(max_length=150)
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        # Add or change the related_name for user_permissions
        # to avoid conflicts
        permissions = models.ManyToManyField(
            'auth.Permission',
            verbose_name='user permissions',
            blank=True,
            related_name='custom_user_set',
            related_query_name='custom_user'
        )

class LoginUserInfo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='login_user_info'
    )
    email = models.CharField(max_length=150)
    session = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
