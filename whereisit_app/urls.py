from django.urls import path

from . import views


urlpatterns = [
path('item/add/', views.ItemCreateView.as_view(), name='item-create'),
path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
path('item/<int:pk>/update', views.ItemUpdateView.as_view(), name='item-update'),
path('item/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
path('item/search/', views.search, name='item-search'),
]
