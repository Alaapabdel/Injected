from django.db import models

# Create your models here.
class User(models.Model):
    username= models.CharField(max_length=100)
    password= models.CharField(max_length=100)
    cc= models.CharField(max_length=19,default='', blank=True)
    def __str__(self):
        return self.username