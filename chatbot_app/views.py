import requests
import json
from django.http import JsonResponse
from .models import User, Chat
def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        
        # Generate user_id by incrementing the last user_id
        last_user = User.objects.order_by('-user_id').first()
        user_id = 1 if last_user is None else last_user.user_id + 1

        # Create a new User object
        user = User.objects.create(user_id=user_id, name=name, phone_number=phone_number)
        
        return JsonResponse({'user_id': user_id})
    return JsonResponse({'error': 'Invalid request method'})

def chatbot(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        query = request.POST['query']

        user, created = User.objects.get_or_create(user_id=user_id)

        chat = Chat.objects.create(user=user, chat_id=user_id, query=query)

        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': 'Bearer YOUR_API_KEY',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                             {'role': 'user', 'content': query}],
                'max_tokens': 50
            }
        )

        bot_response = response.json()['choices'][0]['message']['content']
        chat.response = bot_response
        chat.save()

        return JsonResponse({'response': bot_response})
    return JsonResponse({'error': 'Invalid request method'})
