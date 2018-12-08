from django.urls import path
from . import views


urlpatterns = [
	path('parameters', views.parameters, name='parameters'),
	path('textures', views.textures, name='textures'),
        path('selection', views.selection, name='selection'),        
]

