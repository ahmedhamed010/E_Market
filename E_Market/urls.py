from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from order.views import add_to_cart , get_cart 
from account.views import *

urlpatterns = [     
    path('admin/', admin.site.urls),
    
    path('api/', include('products.urls')),
        # تسجيل مستخدم جديد & وعرض المستخدم
    path('account/', include('account.urls')),
    
    path('order/', include('order.urls')),
    
        # تسجيل الدخول (الحصول على JWT Token) & وتجديد التوكين 
    path('api/token/', TokenObtainPairView.as_view() , name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # path("__debuge__/",include("debug_toolbar.urls")),
    path('cart/add/', add_to_cart,name='add_to_cart'),
    path('get/cart/', get_cart,name='get_cart'),

    path('forgot-password/' , forgot_password , name='forgot_password'),
    path('reset-password/' , reset_password , name='reset_password'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'utils.error_view.handler404'
handler500 = 'utils.error_view.handler500'
send_mail = 'utils.email_utils.send_mail'
