from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import NotAuthenticated
from app01.token_module import out_token
from rest_framework import HTTP_HEADER_ENCODING


def get_authorization_header(request):
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


def get_userinfo_header(request):
    auth = request.META.get('HTTP_USERINFO', b'')
    if isinstance(auth, type('')):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class TokenAuth1(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request)
        user = get_userinfo_header(request)
        if not auth:
            return None
        token = auth.decode()
        name = user.decode()
        token_obj = out_token(name, token)
        if token_obj:
            return name, token
        else:
            raise NotAuthenticated("登陆信息异常")
