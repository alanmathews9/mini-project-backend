from django.db import models
from basic_auth.models import People


class Chat(models.Model):
    user_email = models.ForeignKey(People, on_delete=models.CASCADE, to_field='email', db_column='user_email')
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat'
