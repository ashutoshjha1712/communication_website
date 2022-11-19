from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=64)
    #status = models.IntegerField(dafault=1)

    def __str__(self):
        return self.name