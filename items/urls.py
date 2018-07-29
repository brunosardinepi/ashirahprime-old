from django.urls import path

from . import views


app_name = 'items'
urlpatterns = [
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('<int:item_pk>/equip/<int:character_pk>/', views.EquipItemView.as_view(), name='equip_item'),
    path('', views.ItemListView.as_view(), name='item_list'),
]