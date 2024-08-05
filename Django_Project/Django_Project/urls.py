from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stockdata.urls')),  # stockdata 앱의 URL 설정을 포함
]