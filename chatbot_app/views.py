import requests
import json
from django.http import JsonResponse
from .models import User, Chat

def chatbot(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        query = request.POST['query']
        
        # Retrieve or create the user based on user_id
        user, created = User.objects.get_or_create(user_id=user_id)
        
        # Create a new chat entry
        chat = Chat.objects.create(user=user, chat_id=user_id, query=query)
        
        # Make a request to the ChatGPT API to get the bot's response
        # Replace 'YOUR_API_KEY' with your actual API key
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': 'Bearer YOUR_API_KEY',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',  # Specify the desired language model
                'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                             {'role': 'user', 'content': query}],
                'max_tokens': 50
            }
        )
        
        # Store the full API response as a string in bot_response
        bot_response = json.dumps(response.json())
        
        # Update the chat entry with the bot's response
        chat.response = bot_response
        chat.save()
        
        # Return a JSON response with the bot's response
        return JsonResponse({'response': bot_response})
    
    # Return an error response for non-POST requests
    return JsonResponse({'error': 'Invalid request method'})
