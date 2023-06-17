from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User, Group, Permission


class Center(models.Model):
    center_name = models.CharField(max_length=100)
    start_hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    start_minute = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    end_hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    end_minute = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    applicants = models.ManyToManyField(User, related_name='centers')

    def __str__(self):
        return self.center_name
