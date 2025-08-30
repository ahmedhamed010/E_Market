from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [     
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
        # تسجيل مستخدم جديد & وعرض المستخدم
    path('account/', include('account.urls')),
    
    path('order/', include('order.urls')),
    
        # تسجيل الدخول (الحصول على JWT Token) & وتجديد التوكين 
    path('api/token/', TokenObtainPairView.as_view() , name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'utils.error_view.handler404'
handler500 = 'utils.error_view.handler500'
