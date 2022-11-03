from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):

    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile.jpg',upload_to='profile_pictures')
    contact_number = models.CharField(max_length=100,default='09051485282')
 

 
class Contact(models.Model):
    fullname = models.CharField(max_length=20, null=True)
    phonenumber = models.CharField(max_length=11, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email