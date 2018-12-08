from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('leroy/', include('leroy.urls')),
	path('admin/', admin.site.urls)
]
