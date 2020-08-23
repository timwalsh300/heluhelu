from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Book(models.Model):
    """Model representing a book"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    goodreads_id = models.CharField(max_length=20)
    image = models.CharField(max_length=200)
    owner = models.ManyToManyField(User, related_name='books', help_text='Who has this book in their collection?')
    favorite = models.ManyToManyField(User, related_name='favorites', help_text='Who marks this book as a favorite in their collection?')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
