from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('recruiter', 'Recruiter'),
        ('job_seeker', 'Job Seeker'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"
