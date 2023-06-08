from django.utils.deprecation import MiddlewareMixin
from .userstore import get_user
from chatbot_project import error_msg_handler

import json
import logging

logger = logging.getLogger(__name__)

excluse_path_list = ['/login', '/logout', '/register_user', '/login/', '/logout/', '/register_user/']

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            request.data = json.loads(request.body.decode('utf-8'))
        except BaseException as e:
            logger.error('Failed to parse json request {}. Reason: {}'.format(request.body, str(e)))
            return error_msg_handler('Failed to parse request body')

        if request.path in excluse_path_list:
            return None

        if 'session_id' not in request.data:
            logger.error('Got request without session_id field. Request {}'.format(request.body))
            return error_msg_handler('session_id not prasent in request')

        session_id = int(request.data['session_id'])
        user = get_user(session_id)
        if not user:
            logger.error('Got request with invalid session_id field. Request {}'.format(request.body))
            return error_msg_handler('not a valid session_id')

        request.user =  user
        return None