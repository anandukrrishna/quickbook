from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)

    description = models.TextField()

    venue = models.CharField(max_length=255)

    date = models.DateTimeField()

    total_seats = models.PositiveIntegerField()

    available_seats = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.available_seats is None:
            self.available_seats = self.total_seats

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title