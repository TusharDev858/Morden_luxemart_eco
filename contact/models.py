from django.db import models


class ContactMessage(models.Model):
    STATUS = [('new', 'New'), ('read', 'Read'), ('replied', 'Replied')]
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
