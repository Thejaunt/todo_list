from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=True, default='')
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['done']
