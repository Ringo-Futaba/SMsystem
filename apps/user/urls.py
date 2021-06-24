from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import LoginView, MemberShowView, LoginOutView, ReSetPasswordView, ReSetPwdView,LoginFailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('membershow/', login_required(MemberShowView.as_view()), name='membershow'),
    path('loginout/', login_required(LoginOutView.as_view()), name='loginout'),
    path('login_reset_password/', ReSetPasswordView.as_view(), name='reset'),
    path('login_reset_pwd/<token>', ReSetPwdView.as_view(), name='reset_pwd'),
    path('login_fail/', LoginFailView.as_view(), name='login_fail')
]
