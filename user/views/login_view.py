import json
from oauth2_provider.signals import app_authorized
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.views.base import TokenView
from oauth2_provider.models import get_access_token_model
from oauth2_provider.views import TokenView # as OAuth2TokenView
from django.http import HttpResponse

from user.models import User


class CustomTokenView(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            body = json.loads(body)
            access_token = body.get("access_token")
            print("access_token", access_token)
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)
                app_authorized.send(sender=self, request=request,token=token)
                body.pop("refresh_token")
                body['user_id'] = str(token.user.user_id)
                body['username'] = str(token.user.username)
                body['email'] = token.user.email
                body['role'] = token.user.role
                body['phone'] = str(token.user.phone)
                body['full_name'] = get_full_name(token.user)
                body = json.dumps(body)
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response
    

def get_full_name(user:User):
    full_name = ""
    if user.first_name:
        full_name = full_name + user.first_name + " "
    if user.last_name:
        full_name = full_name + user.last_name

    full_name = full_name.strip()
    return full_name

    
