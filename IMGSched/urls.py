from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="index"),
        path('login/',auth_views.LoginView.as_view(template_name='registration/login.html')),
        path('userlist/',views.UserViewSet.as_view()),
        path('userlist/<int:pk>',views.UserDetail.as_view()),
        path('rest-auth/',include('rest_auth.urls')),
        path('profile/',views.profile,name="profile"),
        path('auth/',include('social_django.urls', namespace='social')),
        path('test/', views.MeetingViewSet.as_view()),
        path('test/<int:pk>',views.MeetingDetail.as_view()),
        path('comment/<int:fk>',views.CommentView.as_view()),
]