from django.contrib import admin
from django.urls import path,include
from products.views import IndexView
from django.conf import settings
from django.conf.urls.static import static

from users.views import CustomPasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(extra_context={'title':'Storee'}),name= 'index'),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
