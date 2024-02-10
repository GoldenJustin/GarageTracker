from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from PIL import Image
import os

class Owner(models.Model):
    owner_code = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)  # Use a PasswordField
    if_logged = models.BooleanField(default=False)  # Use snake_case for field names
    token = models.CharField(max_length=500, null=True, blank=True)
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=50, choices=(("Male", "Male"), ("Female", "Female")), default="Male")
    avatar = models.ImageField(upload_to="owner-avatars/", null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    def __str__(self):
        return f"{self.owner_code} - {self.first_name} " + (f"{self.middle_name} {self.last_name}" if self.middle_name else f"{self.last_name}")

    def name(self):
        return f"{self.first_name} " + (f"{self.middle_name} {self.last_name}" if self.middle_name else f"{self.last_name}")

    def save(self, *args, **kwargs):
        self.owner_code = self.owner_code.upper()
        self.first_name = self.first_name.upper()
        self.middle_name = self.middle_name.upper() if self.middle_name else None
        self.last_name = self.last_name.upper()
        self.gender = self.gender.upper()
        self.programme = self.programme.upper() if self.programme else None
        first_initial = self.first_name[0].upper()  # Get the initial capital letter of the first name
        last_name = self.last_name[0].capitalize() + self.last_name[1:].lower()  # Capitalize the first letter of the last name        

        super().save(*args, **kwargs)

        if self.avatar:
            imag = Image.open(self.avatar.path)
            if imag.width > 200 or imag.height > 200:
                output_size = (200, 200)
                imag.thumbnail(output_size)
                imag.save(self.avatar.path)

                # Rename the uploaded image file
                avatar_name = f"{self.signature}_photo.png"
                avatar_path = os.path.join("owner-avatars", avatar_name)
                os.rename(self.avatar.path, os.path.join(settings.MEDIA_ROOT, avatar_path))
                self.avatar.name = avatar_path
                self.save(update_fields=['avatar'])

    @property
    def username(self):
        return self.owner_code
    
@receiver(pre_delete, sender=Owner)
def delete_owner_files(sender, instance, **kwargs):

    # Delete the avatar image if it exists
    if instance.avatar:
        avatar_path = os.path.join(settings.MEDIA_ROOT, instance.avatar.name)
        if os.path.exists(avatar_path):
            os.remove(avatar_path)


class technician(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=50)
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")

    def __str__(self):
        return f"{self.username} - {self.email}"