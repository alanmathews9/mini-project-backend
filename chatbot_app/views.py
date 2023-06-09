import requests
import json
from django.http import JsonResponse
from .models import Chat
from basic_auth.models import People

def get_history(request):
    if request.method == 'GET':
        email_id = request.data.get('email_id')

        chat_history = Chat.objects.filter(user_email=email_id)
        
        query_response_pairs = []
        for chat in chat_history:
            query_response_pairs.append({
                'query': chat.query,
                'response': chat.response,
            })
        
        if query_response_pairs:
            return JsonResponse({'email_id': email_id, 'history': query_response_pairs})
        else:
            return JsonResponse({'error': 'No chat history found for the provided email ID.'})
    
    return JsonResponse({'error': 'Invalid request method'})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def chatbot(request):
    if request.method == 'POST':
        if 'user_email' not in request.data:
            return JsonResponse({'error': 'user_email is required'}, status=400)

        user_email = request.data['user_email']
        query = request.data.get('query', '')

        try:
            user = People.objects.get(email=user_email)
        except People.DoesNotExist:
            return JsonResponse({'error': 'Invalid user'}, status=400)

        chat_history = Chat.objects.filter(user_email=user.email).order_by('-id')[:5][::-1]

        messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        for chat in chat_history:
            messages.append({'role': 'user', 'content': chat.query})
            messages.append({'role': 'assistant', 'content': chat.response})

        messages.append({'role': 'user', 'content': query})
        # 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
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': 'Bearer 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',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': messages,
                'max_tokens': 50
            }
        )

        bot_response = response.json()['choices'][0]['message']['content']
        chat = Chat.objects.create(user_email=user, query=query, response=bot_response)

        query_response = [{'query': chat.query, 'response': chat.response} for chat in chat_history]

        query_response.append({'query': query, 'response': bot_response})

        return JsonResponse({
            'user_email': user_email,
            'query_response_pairs': query_response
        })

    return JsonResponse({'error': 'Invalid request method'})
