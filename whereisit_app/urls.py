from django.urls import path

from . import views


urlpatterns = [
path('add/', views.ItemCreateView.as_view(), name='item-create'),
path('<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
path('<int:pk>/update', views.ItemUpdateView.as_view(), name='item-update'),
path('<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
path('search/', views.search, name='item-search'),
path('map/', views.map_location, name='item-map'),
]
