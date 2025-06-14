from django.urls import path
from django.contrib import admin


from rest_framework.routers import SimpleRouter
from .views import BannerView,Company_detailView,NoticeView,ActivityView,LoginView,ActivityJoinView,Map_detailView,Copyright_View



router = SimpleRouter()
router.register('banner', BannerView, 'banner')
router.register('company_detail', Company_detailView, 'company_detail')
router.register('notice', NoticeView, 'notice')
router.register('activity', ActivityView, 'activity')
router.register('user', LoginView, 'user')
router.register('join', ActivityJoinView, 'join')
router.register('map', Map_detailView, 'map')
router.register('copyright', Copyright_View, 'copyright')
urlpatterns = [

]
urlpatterns+= router.urls