from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip')
    destination = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    #Indexes
    class Meta:
        indexes = [
            models.Index(fields=['user'], name='trip_user_idx'),
            models.Index(fields=['start_date'], name='trip_start_date_idx'),
            models.Index(fields=['end_date'], name='trip_end_date_idx'),
        ]

    def __str__(self):
        return f"{self.destination} ({self.start_date} - {self.end_date})"

class Review(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    date_posted = models.DateTimeField(auto_now_add=True)

    #Indexes
    class Meta:
        indexes = [
            models.Index(fields=['trip'], name='review_trip_idx'),
            models.Index(fields=['user'], name='review_user_idx'),
        ]

    def __str__(self):
        return f"Review by {self.user.username} for {self.trip.destination}"

# class Photo(models.Model):
#     trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='photos')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
#     image = models.ImageField(upload_to='trip_photos/')
#     caption = models.CharField(max_length=255, blank=True, null=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Photo by {self.user.username} for {self.trip.destination}"
