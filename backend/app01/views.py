from django.shortcuts import render
from django.http.response import JsonResponse,HttpResponse
from rest_framework.views import APIView
from app01 import models
from app01.token_module import get_token,out_token


# Create your views here.

class AuthLogin(APIView):
    def post(self, request):
        # response = {"code": 100, "msg": None}
        username = request.data.get("username")
        pwd = request.data.get("password")
        user = models.Users.objects.filter(username=username, password=pwd).first()
        response = {
            'meta': {
                'status': 200,
                'msg': '',
            }
        }
        if user:
            token = get_token(username)
            models.Users.objects.update_or_create(username=username, defaults={"token": token})
            response['meta']['msg'] = '登陆成功'
            response['data'] = {
                'email': user.email,
                'rid': user.rid,
                'token': bytes.decode(token),
                'username': user.username,
                'mobile': user.mobile,
            }
        else:
            response['meta']['msg'] = '用户名或密码错误'
            response['meta']['status'] = 1000
        return JsonResponse(response)