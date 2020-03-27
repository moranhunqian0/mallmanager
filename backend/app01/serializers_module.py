from rest_framework import serializers
from app01.models import Users,MenuList,Submenu,UserType


# class UserTypeSerialize(serializers.ModelSerializer):
#     class Meta:
#         model = UserType
#         fields = ['title']


class UsersSerialize(serializers.ModelSerializer):
    # roles = UserTypeSerialize(many=True)
    roles = serializers.CharField(read_only=True,source='ut.title')
    password = serializers.CharField(write_only=True)
    rid = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['id', 'rid','username','password','mobile', 'email', 'ut', 'mg_state', 'roles']
        read_only_fields = ('id', )


class SubmenuSerialize(serializers.ModelSerializer):
    class Meta:
        model = Submenu
        fields = '__all__'


class MenuListSerialize(serializers.ModelSerializer):
    submenu = SubmenuSerialize(many=True,read_only=True)

    class Meta:
        model = MenuList
        fields = ['mid','name','path','submenu']
