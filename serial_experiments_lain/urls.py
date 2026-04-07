from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Todas as rotas do arquivo bots/urls.py estarão acessíveis a partir de /api/bots/
    path('api/bots/', include('bots.urls')), 
]