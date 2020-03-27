from rest_framework.views import APIView
from app01 import models
from app01.token_module import get_token,out_token
from app01.authentication_module import TokenAuth1
import app01.serializers_module as sm
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.forms.models import model_to_dict

# rest_framework 的Response可以直接序列化字典和字符串

# Create your views here.


def str2bool(v):
    return v.lower() in ['true',]


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
            token = bytes.decode(get_token(username))
            models.Users.objects.update_or_create(username=username, defaults={"token": token})
            response['meta']['msg'] = '登陆成功'
            response['data'] = {
                'email': user.email,
                'rid': user.rid,
                'token': token,
                'username': user.username,
                'mobile': user.mobile,
            }
        else:
            response['meta']['msg'] = '用户名或密码错误'
            response['meta']['status'] = 1000
        return Response(response)


class TokenVerify(APIView):
    def post(self, request):
        username = request.data.get("username")
        token = request.data.get("token")
        user = models.Users.objects.filter(username=username).first()
        if user.token == token:
            response = {'code': 200}
        else:
            response = {'code': 1000}
        return Response(response)


class Users(APIView):
    authentication_classes = [TokenAuth1]

    def post(self,request):
        # username = request.data.get("username")
        # pwd = request.data.get("password")
        # mobile = request.data.get("mobile")
        # email = request.data.get("email")
        # rid = models.Users.objects.all().count() + 1
        # token = 1
        # ut = 2
        rid = models.Users.objects.all().count() + 1
        userinfo = request.data
        userinfo.update(rid=rid,token='1',ut=2)
        ser = sm.UsersSerialize(data=userinfo)
        print(userinfo)
        ser.is_valid()
        ser.save()
        return Response({"code": 100, "msg": None})


    def get(self,request):
        query = request.query_params.get("query")
        pagesize = request.query_params.get("pagesize")
        # DRF分页器最基本用法
        page = PageNumberPagination()
        page.page_size = pagesize
        page.page_query_param = "pagenum"
        if len(query)==0:
            user_list = models.Users.objects.all()
        else:
            user_list = models.Users.objects.filter(username__contains=query)
        res = self.query_item(request, user_list, page)
        return Response(res)

    def query_item(self,request,user_list,page):
        res = {"code": 100, "msg": None}
        res["total"] = user_list.count()
        page_list = page.paginate_queryset(user_list, request, view=self)
        ser = sm.UsersSerialize(page_list, many=True)
        res['data'] = ser.data
        return res


class Menu(APIView):
    authentication_classes = [TokenAuth1]

    def get(self,request):
        menu_list = models.MenuList.objects.all()
        ser = sm.MenuListSerialize(menu_list,many=True)
        return Response(ser.data)


class SetState(APIView):
    authentication_classes = [TokenAuth1]

    def put(self,reuqest,id,type):
        booltype = str2bool(type)
        models.Users.objects.filter(id=id).update(mg_state=booltype)
        res = {"code": 200, "msg": None}
        return Response(res)


class UpdateUsers(APIView):
    def put(self,request,username):
        mobile = request.data["mobile"]
        email = request.data["email"]
        models.Users.objects.filter(username=username).update(mobile=mobile,email=email)
        res = {"code": 200, "msg": None}
        return Response(res)

    def delete(self,request,username):
        models.Users.objects.filter(username=username).delete()
        res = {"code": 200, "msg": None}
        return Response(res)