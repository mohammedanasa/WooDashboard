from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    MANAGER = 'Manager'
    COURIER = 'Courier'
    STAFF = 'Staff'
    USER_TYPE_CHOICES = [
        (MANAGER, 'Manager'),
        (COURIER, 'Courier'),
        (STAFF, 'Staff'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=STAFF,
    )
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name()
