from django.db import models

# Create your models here.


class Bank(models.Model):
    bank_code = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=50)

    def __str__(self):
        return self.bank_code
