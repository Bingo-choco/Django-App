
from django.contrib import admin
from django.urls import path

import myapp
from myapp import views

urlpatterns = [

   #初始化页面
    path('', views.index),

   #登录页面
    path('login/', views.login),

   #注册页面
    path('register/', views.register),

   #注销页面
    path('delete/',views.delete),

   #个人信息展示页面
    path('self_center/', views.self_center),

   #个人信息修改页面
    path('change_self/', views.change_self),

   #旅行计划页面
   path('plan_init/', views.plan_init),

   #旅行计划换一批页面
   path('change_plan/', views.change_plan),

   #旅行计划顺序页面
   path('plan_order/', views.plan_order),

   #客户评论反馈
   path('comment/', views.comment),

   #日记生成页面
   path('diary/' , views.diary),

   #问答系统页面
   path('question/', views.question),

    # 问答系统页面
   path('re_ask/', views.re_ask),

   ]

