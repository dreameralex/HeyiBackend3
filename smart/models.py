from django.db import models

# Create your models here.


# 开启app广告页面
class Welcome(models.Model):
    img = models.ImageField(upload_to='welcome', default='/welcome/welcome.jpg', verbose_name='图片')
    order = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)







class Banner(models.Model):

    img = models.ImageField(upload_to='banner', default='banner1.png', verbose_name='图片')

    order = models.IntegerField(verbose_name='顺序')

    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name_plural = '轮播图'


class Notice(models.Model):

    title = models.CharField(max_length=64, verbose_name='公共标题')

    content = models.TextField(verbose_name='内容')

    img = models.ImageField(upload_to='notice', default='notice.png', verbose_name='公告图片')

    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')


    class Meta:
        verbose_name_plural = '公告表'


    def __str__(self):
        return self.title

# 首页公司介绍表
class Company_Detail(models.Model):
    img_header = models.ImageField(upload_to='company_datail', default='/banner1.png', verbose_name="标题图片")
    img_detail_header = models.ImageField(upload_to='company_datail', default='/banner1.png', verbose_name="介绍内容标题图片")
    img_detail_detail = models.ImageField(upload_to='company_datail', default='/banner1.png', verbose_name="介绍内容图片")
    name = models.CharField(max_length=100, verbose_name='介绍标题')
    order = models.IntegerField(verbose_name="顺序")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        verbose_name_plural = "介绍表"

    def __str__(self):
        return self.name

##表模型
class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    avatar = models.FileField(verbose_name="头像", max_length=128, upload_to='avatar')
    create_date = models.DateField(verbose_name="日期", auto_now_add=True)
    score = models.IntegerField(verbose_name="积分", default=0)

    # 用户用手机号登录，手机号
    mobile = models.CharField(verbose_name="手机号",max_length=11,null=True)

    class Meta:
        verbose_name_plural = '用户表'
    def __str__(self):
        return self.name

#  活动表
class Activity(models.Model):
    title = models.CharField(verbose_name="活动标题", max_length=128)
    text = models.TextField(verbose_name="活动描述", null=True, blank=True)
    date = models.DateField(verbose_name="举办活动日期")

    count = models.IntegerField(verbose_name='报名人数', default=0)
    total_count = models.IntegerField(verbose_name='总人数', default=0)
    score = models.IntegerField(verbose_name="积分", default=0)
    info_img = models.ImageField(upload_to='activity', default='/default.png',verbose_name="活动图片")

    join_record = models.ManyToManyField(verbose_name="参与者",
                                         through="JoinRecord",
                                         through_fields=("activity", "user"),
                                         to="UserInfo")

    class Meta:
        verbose_name_plural = '活动表'

    def __str__(self):
        return self.title

#  活动报名记录
class JoinRecord(models.Model):
    user = models.ForeignKey(verbose_name='用户', to="UserInfo", on_delete=models.CASCADE)
    activity = models.ForeignKey(verbose_name="活动", to="Activity", on_delete=models.CASCADE, related_name='ac')
    point = models.IntegerField(verbose_name="活动积分", default=0)
    participation = models.BooleanField(verbose_name="是否已参加", default=False)
    exchange = models.BooleanField(verbose_name="是否已兑换", default=False)

    class Meta:
        verbose_name_plural = '活动报名记录'



# 地图
class Map(models.Model):
    title = models.CharField(verbose_name="活动标题", max_length=128)
    map_detail = models.ImageField(upload_to='map', verbose_name="地图")
    order = models.IntegerField(verbose_name="顺序")
    class Meta:
        verbose_name_plural = '地图'

    def __str__(self):
        return  self.title

# 版权
class Copyright(models.Model):
    title = models.CharField(verbose_name="版权标题", max_length=50)
    img = models.ImageField(upload_to='copyright', verbose_name="版权图片")
    description = models.CharField(verbose_name="版权信息", max_length=250)
    categoryName = models.CharField(verbose_name="版权类别", max_length=50)
    order = models.IntegerField(verbose_name="顺序",auto_created=True)
    img_detail = models.ImageField(upload_to='copyright/copyright_detail',default='/default.png', verbose_name="版权图片")
    class Meta:
        verbose_name_plural = '版权'
    def __str__(self):
        return  self.title

#轮播图2
class Banner_Goods_type(models.Model):
    type = models.CharField(verbose_name="商品类别", max_length=50)
    class Meta:
        verbose_name_plural = '商品类别'
    def __str__(self):
        return self.type


class Banner_Goods(models.Model):
    name = models.CharField(verbose_name="商品名称", max_length=50)
    type = models.ForeignKey(Banner_Goods_type, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='banner_goods', verbose_name="商品图片")
    description = models.CharField(verbose_name="商品详情", max_length=250)
    order = models.IntegerField(verbose_name="顺序")
    class Meta:
        verbose_name_plural = '商品轮播图'

    def __str__(self):
        return self.name








