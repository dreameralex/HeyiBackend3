from django.contrib import admin

# Register your models here.
from .models import Banner, Notice,Company_Detail,Activity,UserInfo,Map,Copyright,Banner_Goods,Banner_Goods_type,Banner,Welcome,JoinRecord

admin.site.register(Banner)
admin.site.register(Notice)
admin.site.register(Company_Detail)
admin.site.register(Activity)
admin.site.register(UserInfo)
admin.site.register(Map)
admin.site.register(Copyright)
admin.site.register(Banner_Goods)
admin.site.register(Banner_Goods_type)
admin.site.register(Welcome)
admin.site.register(JoinRecord)