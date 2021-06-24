from django.contrib import admin
from django.urls import path, include
from .views import IndexView, GoodsShowView, WelcomeView, GoodsUpdateStatus, GoodsDeleteView, GoodsInsertView, GoodsImgUpView, GoodsUpdateInfoView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),
    path('show/', login_required(GoodsShowView.as_view()), name='show'),
    path('welcome/', login_required(WelcomeView.as_view()), name='welcome'),
    path('GoodsUpdateStatus/', login_required(GoodsUpdateStatus.as_view()), name='updateStatus'),
    path('GoodsDeleteView/', login_required(GoodsDeleteView.as_view()), name='deleteGoods'),
    path('GoodsInsertView/', login_required(GoodsInsertView.as_view()), name='insertGoods'),
    path('GoodsImgUpView', login_required(GoodsImgUpView.as_view()), name='imgUp'),
    path('goods_update/', login_required(GoodsUpdateInfoView.as_view()), name='updateGoods')

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
