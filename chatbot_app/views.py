import requests
import json
from django.http import JsonResponse
from .models import Chat
from basic_auth.models import People

from django.db import connection
from django.http import JsonResponse

def get_history(request):
    if request.method == 'GET':
        email_id = request.GET.get('email_id')

        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT id, query, response
                FROM chat
                WHERE user_email = %s
                ORDER BY id DESC
                ''',
                [email_id]
            )
            chat_history = cursor.fetchall()

        query_response_pairs = []
        for chat in chat_history:
            query_response_pairs.append({
                'query': chat[1],
                'response': chat[2]
            })

        if query_response_pairs:
            return JsonResponse({'email_id': email_id, 'history': query_response_pairs})
        else:
            return JsonResponse({'error': 'No chat history found for the provided email ID.'})

    return JsonResponse({'error': 'Invalid request method'})


def chatbot(request):
    if request.method == 'POST':
        user_email = request.POST['user_email']
        query = request.POST['query']

        user, created = People.objects.get_or_create(email=user_email)

        chat_history = Chat.objects.filter(user_email=user.email).order_by('-id')[:5][::-1]

        messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        for chat in chat_history:
            messages.append({'role': 'user', 'content': chat.query})
            messages.append({'role': 'assistant', 'content': chat.response})

        messages.append({'role': 'user', 'content': query})

        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': 'Bearer <YOUR_API_KEY>',
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
