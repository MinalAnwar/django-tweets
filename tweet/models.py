from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    #To tweets only from the registered users 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at =  models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.text[:20]}'
     
