from django.db import models

# Create your models here.
class Recipe(models.Model):
    name= models.CharField(max_length=50)
    ingredients= models.TextField()
    cooking_time= models.IntegerField()
    difficulty= models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.name)