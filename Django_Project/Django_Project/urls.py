from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stocks/', include('stockdata.urls')),
    path('', views.home, name='home'),  # 빈 경로에 대한 URL 패턴을 추가합니다.
]