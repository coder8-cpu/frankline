from django.db import models

# Create your models here.

class Contact(models.Model):

    name     =      models.CharField(max_length=1000)
    mobileno =      models.CharField(max_length=1000)
    inquery  =      models.CharField(max_length=1000)
    msg      =      models.CharField(max_length=1000)
    email    =      models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.name
    
class Dealer(models.Model):

    name     =      models.CharField(max_length=1000)
    mobileno =      models.CharField(max_length=1000)
    city     =      models.CharField(max_length=1000)
    msg      =      models.CharField(max_length=1000)
    email    =      models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.name
    