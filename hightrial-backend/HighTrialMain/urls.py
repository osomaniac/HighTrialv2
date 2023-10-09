from django.urls import path, include
from . import views
from .views import SignUpView

app_name = 'hightrial'

urlpatterns = [
    path('',views.index, name='index'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('users/<int:owner_id>/', views.userProfile, name="profile")
]