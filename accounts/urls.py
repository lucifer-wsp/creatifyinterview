from django.urls import path
from . import views

urlpatterns = [
    # 异步认证端点
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('me/', views.me, name='me'),
]
