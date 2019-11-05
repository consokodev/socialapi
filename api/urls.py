"""socialapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from api.views import CreateUser, LoginUser, HelloView, LoginUserFace, LogoutUser, UpdateUser,UserResetPass

urlpatterns = [
    path('user/', CreateUser.as_view(), name='createuser'),
    path('user/email/', LoginUser.as_view(), name='loginuser'),
    path('user/fb/', LoginUserFace.as_view(), name='loginuserface'),
    path('user/logout/', LogoutUser.as_view(), name='logout'),
    path('user/update/', UpdateUser.as_view(), name='update'),
    path('user/resetpass/', UserResetPass.as_view(), name='resetpass'),
    path('hello/', HelloView.as_view(), name='hello'),
]
