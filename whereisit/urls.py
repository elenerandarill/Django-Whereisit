"""whereisit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from whereisit_app import views
from whereisit_app.views import ItemListView, ItemDetailView, ItemCreateView, ItemDeleteView, ItemUpdateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', ItemListView.as_view(), name='home'),
    # Authorization.
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='whereisit_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='whereisit_app/logout.html'), name='logout'),
    # User.
    path('profile/', views.profile, name='profile'),
    #Items.
    path('item/add/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/<int:pk>/update', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    #Admin.
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)