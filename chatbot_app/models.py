from django.db import models
from basic_auth.models import User


class Chat(models.Model):
    chat_id = models.IntegerField()
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
