from django.db import models

# Create your models here.
class Account(models.Model):
    Email = models.EmailField( max_length=30, primary_key=True, unique=True)
    Username = models.CharField(max_length=15)
    Password = models.CharField(max_length=20)
    
    def __str__(self):
        return self.Username
