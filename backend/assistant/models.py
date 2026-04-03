from django.db import models


class Document(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    file = models.FileField(upload_to='documents/')
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20)
    file_size = models.PositiveIntegerField()
    extracted_text = models.TextField(blank=True, default='')
    summary = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.filename
