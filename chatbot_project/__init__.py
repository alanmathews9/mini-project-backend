from django.http import HttpResponse
import json

def error_msg_handler(err_msg):
    json_response = { "type": "ErrorMsg", "message": err_msg }
    return HttpResponse(json.dumps(json_response, default=str), content_type="application/json")