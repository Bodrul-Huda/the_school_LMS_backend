from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

USER_ROLE = {
  'admin' : 'Admin',
  'teacher': 'Teacher',
  'student': 'Student'
}

class User(AbstractUser):
  email = models.EmailField(unique=True)
  role = models.CharField(max_length=20, choices=USER_ROLE)
  mobile_no = models.CharField(max_length=20, blank=True)

  def __str__(self):
    return f"{self.username} ({self.role})"