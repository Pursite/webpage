from django.db import models

class Athnticate(models.Model):
    name = models.CharField(max_length=48)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name 
