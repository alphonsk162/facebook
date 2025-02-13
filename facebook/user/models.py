from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=10, null=True)
    last_name = models.CharField(max_length=10, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, default="profile_pics/default_pfp.png"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    location = models.CharField(max_length=100, default="Not Added")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_photo = models.ImageField(
        upload_to="cover_photos/", default="cover_photos/default_cover.png", blank=True
    )
    works_at = models.CharField(max_length=100, default="Not Added")
    relationship_status = models.CharField(max_length=100, default="Not Added")
    mobile_number = models.CharField(max_length=100, default="Not Added")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
