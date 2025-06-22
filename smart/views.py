from django.shortcuts import render

# Create your views here.
from rest_framework.mixins import ListModelMixin

from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from .models import Banner, Notice,Company_Detail

from .serializer import BannerSerializer, NoticeSerializer,Conpany_detailSerializer,MapSerializer


class BannerView(GenericViewSet, ListModelMixin):

    queryset = Banner.objects.all().filter(is_delete=False).order_by('order')[:3]

    serializer_class = BannerSerializer

    def list(self, request, *args, **kwargs):

        res = super().list(request, *args, **kwargs)

        notice = Notice.objects.all().order_by('create_time').first()

        serializer = NoticeSerializer(instance=notice)

        return Response({'code': 100, 'msg': '成功', 'banner': res.data, 'notice': serializer.data})



class Company_detailView(GenericViewSet, ListModelMixin):
    queryset = Company_Detail.objects.all().filter(is_delete=False).order_by('order')[:3]

    serializer_class = Conpany_detailSerializer

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        return Response({'code': 100, 'msg': '成功', 'company_detail': res.data})

# 公告接口
from .models import Notice
from  .serializer import NoticeSerializer

class NoticeView(GenericViewSet, ListModelMixin):
    queryset = Notice.objects.all().order_by('create_time')
    serializer_class = NoticeSerializer

# 活动
from .models import Activity
from .serializer import ActivitySerializer
class ActivityView(GenericViewSet,ListModelMixin):
    queryset =Activity.objects.all().order_by('date')
    serializer_class = ActivitySerializer



from libs.send_tx_sms import get_code,send_sms_by_phone
from django.core.cache import cache
from rest_framework.decorators import action
from .models import UserInfo
from rest_framework_simplejwt.tokens import RefreshToken
from faker import Faker


# 发送短信接口--》快速登录--》普通手机号登陆舰
class LoginView(GenericViewSet):
    # 短信发送频率限制--->drf的频率限制，根据IP或手机号
    @action(methods=['GET'], detail=False)
    def send_sms(self, request, *args, **kwargs):

        # 1 取出前端传入手机号
        mobile = request.query_params.get('mobile')

        # 2 获取随机验证码
        code = get_code()
        print('验证码',code)

        # 3 验证码放到缓存->临时存储，后期可以根据key取出来
        cache.set(f'sms_{mobile}', code)

        # 4 发送短信
        res = send_sms_by_phone(mobile, code)
        if res:
            return Response({'code': 100, 'msg': '短信发送成功'})

        else:
            return Response({'code': 101, 'msg': '短信发送失败，请稍后再试'})

    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        # 1 取出手机号和验证码
        mobile = request.data.get('mobile')
        code = request.data.get('code')

        # 2 校验验证码是否正确
        old_code = cache.get(f'sms_{mobile}')

        if old_code == code:
            # 3 数据库查询用户，如果存在直接签发token登录成功
            user = UserInfo.objects.filter(mobile=mobile).first()

            if not user:
                 # 4 如果用户不存在，创建用户，再签发token --> simple-jwt
                fake = Faker('zh_CN')
                username = fake.name()
                user = UserInfo.objects.create(mobile=mobile, name=username)

            # 5 能查到直接签发
            refresh = RefreshToken.for_user(user)
            return Response(
                 {'code': 100, 'msg': '登录成功', 'token': str(refresh.access_token), 'name': user.name,
                'score': user.score, 'avatar': 'http://192.168.5.6:8000/media/' + str(user.avatar)})

        else:
            return Response({'code': 101, 'msg': '验证码错误'})





    @action(methods=['POST'], detail=False)
    def quick_login(self, request, *args, **kwargs):

        # 1 取出前端传入的code
        code = request.data.get('code')

        # 2 通过code，调用微信开发平台接口，换取手机号

        # 3 拿到手机号再自己库中查，能查到，签发token

        # 4 查不到注册再签发token

        # 假数据---》都签发成第一个用户
        user = UserInfo.objects.filter(pk=1).first()

        refresh = RefreshToken.for_user(user)

        return Response(
            {'code': 100, 'msg': '登录成功', 'token': str(refresh.access_token), 'name': user.name, 'score': user.score,
             'avatar': 'http://192.168.5.6:8000/media/' + str(user.avatar)})

### 报名后端接口
from .auth import MyJSONWebTokenAuthentication

from .models import JoinRecord
class ActivityJoinView(GenericViewSet):
    authentication_classes = [MyJSONWebTokenAuthentication]

    @action(methods=['POST'], detail=False)
    def join(self, request, *args, **kwargs):
        # 1 取出要参加的活动id
        activity_id = request.data.get('id')
        # 2 取出当前登录用户
        user = request.user
        # 2 查到当前活动
        activity = Activity.objects.filter(pk=activity_id).first()
        # 3 判断时间，判断人数
        # 4 判断是否报名过
        join_record = JoinRecord.objects.filter(activity_id=activity_id, user=user).first()
        if join_record:
            return Response({'code': 101, 'msg': "已经报名过，不用重复报名"})
        else:
            # 5 包名人数+1，报名报存入
            activity.count = activity.count + 1
            activity.save()
            JoinRecord.objects.create(activity=activity, user=user)
            # 6 返回报名成功
            return Response({'code': 100, 'msg': "报名成功"})

# 地图后端接口
from .models import Map
class Map_detailView(GenericViewSet, ListModelMixin):
    queryset = Map.objects.all().filter().order_by('order')

    serializer_class = MapSerializer

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        return Response({'code': 100, 'msg': '成功', 'map_detail': res.data})


# 版权后端接口
from .models import Copyright
from .serializer import  CopyrightSerializer
class Copyright_View(GenericViewSet, ListModelMixin):
    queryset = Copyright.objects.all().filter().order_by('order')

    serializer_class = CopyrightSerializer

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        return Response({'code': 100, 'msg': '成功', 'copyrightData': res.data})


from .models import Banner_Goods
from .serializer import Banner_Product_Serializer
class Banner_Product_view(GenericViewSet, ListModelMixin):
    queryset = Banner_Goods.objects.all().filter().order_by('order')

    serializer_class = Banner_Product_Serializer
    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        return Response({'code': 100, 'msg': '成功', 'data': res.data})




# Welcome
from .models import Welcome
from django.http import JsonResponse
def welcome(request):
    res = Welcome.objects.all().order_by('-order').first()
    img = 'http://192.168.5.6:8000/media/' + str(res.img)
    return JsonResponse({'code': 100, 'msg': '成功', 'result': img})