from django.http import HttpResponse
from basic_auth.models import User
from django.views.decorators.csrf import csrf_exempt
import basic_auth.userstore as userstore
import json
import logging
import bcrypt


logger = logging.getLogger(__name__)

@csrf_exempt
def login(request):
    if 'email_id' not in request.data:
        logger.error(
            'Got login request without email field. Request: {}.'.format(request.data))
        return HttpResponse(json.dumps({"type": "LoginResponse", "status": "failure", "reason": "email id not present"}, default=str),
                            content_type="application/json")
    if 'password' not in request.data:
        logger.error(
            'Got login request without password field. Request: {}.'.format(request.data))
        return HttpResponse(json.dumps({"type": "LoginResponse", "status": "failure", "reason": "password id not present"}, default=str),
                            content_type="application/json")

    email_id = request.data['email_id']
    password = request.data['password']
    
    status, msg_or_session_id = userstore.login(email_id, password)
    if status:
       return HttpResponse(json.dumps({"type": "LoginResponse", "status": "success", "session_id": msg_or_session_id}, default=str),
                           content_type="application/json")
    return HttpResponse(json.dumps({"type": "LoginResponse", "status": "failure", "reason": msg_or_session_id}, default=str),
                        content_type="application/json")


@csrf_exempt
def logout(request):
    if 'session_id' not in request.data:
        logger.error(
            'Got logout request without session_id field. Request: {}.'.format(request.data))
        return HttpResponse(json.dumps({"type": "LogOutResponse", "status": "failure", "reason": "session_id not present"}, default=str),
                            content_type="application/json")
    session_id = int(request.data['session_id'])
    if not userstore.logout(session_id):
        logger.error(
            'Got logout request with invalid session_id field. Request: {}.'.format(request.data))
        return HttpResponse(json.dumps({"type": "LogOutResponse", "status": "failure", "reason": "invalid session_id"}, default=str),
                            content_type="application/json")
    return HttpResponse(json.dumps({"type": "LogOutResponse", "status": "success"}, default=str), content_type="application/json")


@csrf_exempt
def register_user(request):
    if 'name' not in request.data:
        logger.error(
            'Got login request without name field. Request: {}.'.format(request.data))
        return HttpResponse(json.dumps({"type": "RegisterResponse", "status": "failure", "reason": "name not present"}, default=str),
                            content_type="application/json")
    if 'email_id' not in request.data:
        logger.error(
            'Got login request without email field. Request: {}.'.format(request.data))
        return HttpResponse(json.dumps({"type": "RegisterResponse", "status": "failure", "reason": "email id not present"}, default=str),
                            content_type="application/json")
    if 'password' not in request.data:
        logger.error(
            'Got login request without password field. Request: {}.'.format(request.data))
        return HttpResponse(json.dumps({"type": "RegisterResponse", "status": "failure", "reason": "password id not present"}, default=str),
                            content_type="application/json")

    name = request.data['name']
    email_id = request.data['email_id']
    password = request.data['password']

    status, err_msg = userstore.register(name, email_id, password)
    if status:
       return HttpResponse(json.dumps({"type": "RegisterResponse", "status": "success"}, default=str),
                           content_type="application/json")
    return HttpResponse(json.dumps({"type": "RegisterResponse", "status": "failure", "reason": err_msg}, default=str),
                        content_type="application/json")

