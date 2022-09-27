from django.db import models


# Create your models here.    
class User(models.Model):
    """Creates User

    Returns:
        A new User class
    """

    email = models.EmailField(max_length=30, primary_key=True, unique=True)
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.Username


class Character(models.Model):
    """Creates characters

    Returns:
        A new character class
    """

    Name = models.CharField(max_length=20)
    AccountOwner = models.ForeignKey(User, on_delete=models.CASCADE)
    Race = models.CharField(max_length=15)
    Class = models.CharField(max_length=9)
    Background = models.CharField(max_length=22)
    Alignment = models.CharField(max_length=17)
    Level = models.IntegerField()
    Experience = models.IntegerField()
    Strength = models.IntegerField()
    Dexterity = models.IntegerField()
    Constitution = models.IntegerField()
    Intelligence = models.IntegerField()
    Wisdom = models.IntegerField()
    Charisma = models.IntegerField()

    def __str__(self):
        return self.Name + " Level " + self.Level + " " + self.Class
