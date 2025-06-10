from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('custom', 'Custom'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    custom_status = models.CharField(max_length=50, blank=True, null=True, help_text="If status is 'Custom', specify here")
    complete = models.BooleanField(default=False)  # Keep this for backward compatibility
    duedate = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Update complete field based on status for backward compatibility
        self.complete = (self.status == 'completed')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['status', 'duedate']  # Show incomplete tasks first, then by due date

#creating the task group model !!
class TaskGroup(models.Model):
    COLOR_CHOICES = [
        ('primary', 'Blue'),
        ('success', 'Green'),
        ('danger', 'Red'),
        ('warning', 'Yellow'),
        ('info', 'Light Blue'),
        ('secondary', 'Gray'),
        ('dark', 'Dark'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('orange', 'Orange'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='primary')
    tasks = models.ManyToManyField(Task, related_name='groups', blank=True)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']