from rest_framework import serializers

from .models import Banner, Notice,Company_Detail,Activity,Map,Copyright,Banner_Goods,Banner_Goods_type


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
        fields = ['id', 'title','text','date','count','score','total_count']
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
        fields = ['order', 'title','img','description','categoryName']



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


