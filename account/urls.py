from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register' , views.RegisterViewSet , basename='register')
router.register('user' , views.CurrentUserViewSet , basename='user')
router.register('update' , views.UpdateUserViewSet , basename='update')

urlpatterns = [
    path('' , include(router.urls)),
    path('forgot_password/' , views.forgot_password , name='forgot_password'),
    path('reset_password/<str:token>' , views.reset_password , name='reset_password'),
]

