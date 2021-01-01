from django.db import models

# Create your models here.


class Bank(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    long_cocde = models.CharField(max_length=120, null=True, blank=True)
    gateway = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.code
