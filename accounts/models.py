from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django_lifecycle import hook, LifecycleModelMixin, AFTER_CREATE, AFTER_UPDATE, BEFORE_CREATE, BEFORE_UPDATE
from django.utils.text import slugify
from easy_thumbnails.fields import ThumbnailerImageField
from common.utils import random_file_name

class GenderChoices(models.TextChoices):
    male = ('Male', 'Male')
    female = ('Female', 'Female')
    other = ('Other', 'Other')

# Create your models here.
class User(LifecycleModelMixin,AbstractUser):
    email = models.EmailField(unique=True)
    change_email = models.EmailField(null=True, blank=True)
    contact_number = PhoneNumberField(null=True, blank=True, unique=True)
    is_username_updated = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True, blank=False, null=True)
    objects = UserManager()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.email
    
    @hook(AFTER_CREATE, when_any=['is_superuser', 'is_staff'], is_now=False, priority=2)
    def create_profile(self):
        UserProfile.objects.create(user=self)
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="One user is relate only with one profile."
    )
    gender = models.CharField(max_length=100, choices=GenderChoices.choices, blank=True, null=True)
    profile_image = ThumbnailerImageField(upload_to=random_file_name, blank=True, null=True)
    
# class Driver(models.Model):
#     profile = models.OneToOneRel(UserProfile,on_delete=models.CASCADE,related_name="user")
#     driving_licence = models.CharField(max_length = 30,null = True,blank = True)
#     image_licence = models.ImageField(upload_to=random_file_name,blank=True,null=True)
#     is_approved = models.BooleanField(default = False)
    
# class Vehicle(models.Model):
#     driver = models.ForeignKey(Driver,on_dele)
    