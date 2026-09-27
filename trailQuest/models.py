from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

DIFFICULTY_LEVEL_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]

TRAIL_TYPE_CHOICES = [
    ('Loop', 'Loop'),
    ('Out & Back', 'Out & Back'),
    ('Point-to-Point', 'Point-to-Point'),
]

APPROVAL_STATUS_CHOICES = [
    ('pending', 'Pending Approval'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

# Create your models here.
class Trail(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=6, blank=True, null=True)
    start_point = models.CharField(max_length=100, blank=True, null=True)
    end_point = models.CharField(max_length=100, blank=True, null=True)
    distance = models.DecimalField(max_digits=18, decimal_places=2, help_text="Distance in kilometers")
    elevation_gain = models.DecimalField(max_digits=18, decimal_places=2, help_text="Elevation gain in meters")
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVEL_CHOICES)
    trail_type = models.CharField(max_length=20, choices=TRAIL_TYPE_CHOICES)
    estimated_time = models.DecimalField(max_digits=18, decimal_places=2, help_text="Estimated time in hours")
    trail_conditions = models.TextField(blank=True, null=True)
    accessibility = models.TextField(blank=True, null=True)
    photos = models.ImageField(upload_to='trail_photos/', null=True, blank=True)
    user_notes = models.TextField(blank=True, null=True)
    date_submitted = models.DateTimeField(default=timezone.now)
    
    # New fields for trail approval management
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_trails')
    admin_comments = models.TextField(blank=True, null=True, help_text="Administrator approval or rejection comments")
    
    def __str__(self):
        return self.name
    
REVIEW_RATING_CHOICES = [
    ('poor', '1 - Poor'),
    ('fair', '2 - Fair'),
    ('good', '3 - Good'),
    ('very good', '4 - Very Good'),
    ('excellent', '5 - Excellent'),
]

class Review(models.Model):
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.CharField(max_length=20, choices=REVIEW_RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.trail.name + " - " + self.user.username