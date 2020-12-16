from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Book(models.Model):
    """Model representing a book"""
    title = models.CharField(max_length=200)
    cover = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    olid = models.CharField(max_length=40)
    owners = models.ManyToManyField(User, related_name='books', help_text='Who has this book in their collection?')
    num_owners = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
