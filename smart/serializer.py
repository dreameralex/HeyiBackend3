import time

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Banner, Notice,Company_Detail,Activity,Map,Copyright,Banner_Goods,Banner_Goods_type,UserInfo

from .utils import *

import datetime
import random

# 轮播图表序列化类

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

# 社区通知序列化类

class NoticeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Notice

        fields = ['id', 'title','img','create_time','content']
        # create_time 到年月日
        extra_kwargs = {
            'create_time': {'format': '%Y-%m-%d'},
        }

class Conpany_detailSerializer(serializers.ModelSerializer):

    class Meta:

        model = Company_Detail

        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title','text','date','count','score','total_count','info_img']
        extra_kwargs={
            'date':{'format':"%Y-%m-%d"}
        }

class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'title','map_detail']

class CopyrightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Copyright
        fields = ['order', 'title','img','description','categoryName','img_detail']



class Banner_Product_type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Banner_Goods_type
        fields = '__all__'

class Banner_Product_Serializer(serializers.ModelSerializer):
    type = Banner_Product_type_Serializer()
    class Meta:
        model = Banner_Goods
        fields = ['type','id', 'name','img','description']
        depth = 1


class  WXAuthUserSerializer(serializers.ModelSerializer):
    phone =  serializers.RegexField(regex=r'^1[3-9]\d{9}$',label='手机号')
    token = serializers.CharField(read_only=True, label='登录态的Token')

    class Meta:

        model = UserInfo
        fields = (
            'id','phone','token','openid','avatar','name'
        )
        # extra_kwargs = {
        #     'openid': {'read_only': True,
        #                'write_only': True,
        #     },
        # }
    def validate(self, attrs):
        #把加密的openid 解密
        openid = attrs.get('openid')
        openid = check_save_user_token(openid)

        if openid is None:
            raise serializers.ValidationError('openid无效 ')
        attrs['openid'] = openid
        phone = attrs.get('phone')
        if UserInfo.objects.filter(phone=phone).count() > 0:
            raise serializers.ValidationError('手机号已经存在')
        if UserInfo.objects.filter(openid=openid).count() > 0:
            raise serializers.ValidationError('改微信已绑定用户')
        return attrs

    def create(self, validated_data):
        validated_data['username'] = str(time.time()) + str(random.randint(1, 9999))
        user = UserInfo.objects.create(**validated_data)

        # 生成JWT
        refresh = RefreshToken.for_user(user)
        user.token = str(refresh.access_token)
        return user