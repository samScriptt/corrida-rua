# corridarua/urls.py (O arquivo principal)

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # 1. Importar as views de auth

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # 2. URLs de Autenticação (Login e Logout)
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    # O LogoutView já funciona "sozinho" com o redirecionamento do settings.py
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), 
    
    # 3. Incluir as URLs do app 'core' na raiz do site
    path("", include("core.urls")), 
]