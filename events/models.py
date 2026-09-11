from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=255)

    description = models.TextField()

    venue = models.CharField(max_length=255)

    date = models.DateTimeField()

    total_seats = models.PositiveIntegerField()

    available_seats = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title