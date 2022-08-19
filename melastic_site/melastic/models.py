from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class MendeleyGroup(models.Model):
    """A Mendeley' group representation(model) in the app database"""
    # Mendeley User to handle the group
    mendeley_username = models.CharField(max_length=250)

    mendeley_password = models.CharField(max_length=250)
    # Mendeley Group Id
    mendeley_id = models.CharField(max_length=36)
    name = models.CharField(max_length=250)
    # endeley URL
    link = models.CharField(max_length=250, default='www.mendeley.com')
    # Mendeley Group access type
    access_level = models.CharField(max_length=20, choices=[('private','private'), ('invite_only','invite_only'), ('public','public')], default='private')
    # Documents in the Group.

    # Categories in the Group

    def __str__(self):
        return self.name

    def documents(self):
        return self.document_set.all()

    def get_docs_amount(self):
        return self.document_set.all().count()

class Document(models.Model):
    """A Document model."""
    mendeley_id = models.CharField(max_length=100, null=True, unique=True)
    title = models.CharField(max_length=256)
    tags = models.CharField(max_length=512)
    websites = models.CharField(max_length=1024, default='')
    abstract = models.TextField(null=True)
    groups = models.ManyToManyField(MendeleyGroup)

    year = models.DateTimeField(default=timezone.now)
    keywords = models.CharField(max_length=250, blank=True)
    author = models.CharField(max_length=100, blank=True)

    classified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')
    
    def get_categories(self):
        return list(self.categories.all)

