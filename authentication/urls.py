from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uid>/<token>', views.activate.as_view(), name="activate")
]
