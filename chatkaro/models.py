from django.db import models

# Create your models here.

class feedback(models.Model):
    name=models.CharField(max_length=20)
    good=models.IntegerField(default=0)
    bad=models.IntegerField(default=0)
    best=models.IntegerField(default=0)
    def __str__(self):
        return self.name