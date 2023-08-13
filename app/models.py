from django.db import models
from django.utils.text import slugify
import random
from django.conf import settings
from .validators import EducationStages
from django.urls import reverse
# Create your models here.

User = settings.AUTH_USER_MODEL

class Family(models.Model):
    relative_choices = [
        ('F','Father'),
        ('M', 'Mother'),
        ('S', 'Son'),
        ('D', 'daughter')
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    birth_date = models.DateField()
    phone = models.CharField(max_length=255, null=True)
    joined_date = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    relative_choices = models.CharField(max_length=1, null=True, choices=relative_choices)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if self.slug is None:
            rand = random.randint(10_000, 50_000)
            self.slug = f'{slugify(self.name)}-{rand}'
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/family/{self.slug}'
    
    def get_hx_url(self):
        return reverse('family:hx-details', kwargs={'slug': self.slug})
    
    def get_update_url(self):
        return reverse('family:update', kwargs={'slug': self.slug})
    
    def get_details_children(self):
        return self.details_set.all()
   

class Details(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    car = models.CharField(max_length=100)
    education = models.CharField(max_length=100, validators=[EducationStages])
    
    def get_hx_edit_url(self):
        kwargs={
            'slug': Family.objects.get(id=self.family_id).slug,
            'id': self.id,
        }
        return reverse('family:hx-detail-details', kwargs=kwargs)
    