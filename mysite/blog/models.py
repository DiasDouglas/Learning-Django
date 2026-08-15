from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=250)
    # 'Slug' is a short label ("Learning Python: So fun" --> "learning-python-so-fun")
    slug = models.SlugField(max_length=250)     
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # This class defines metadata for the model
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']) # index ordering is not supported on MySQL
        ]

    def __str__(self):
        return self.title