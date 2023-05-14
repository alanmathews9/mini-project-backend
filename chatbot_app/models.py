from django.db import models

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_id = models.IntegerField()
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)