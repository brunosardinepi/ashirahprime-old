from django.urls import path

from . import views


app_name = 'items'
urlpatterns = [
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('<int:pk>/equip/', views.EquipItemView.as_view(), name='equip_item'),
    path('<int:pk>/unequip/', views.UnequipItemView.as_view(), name='unequip_item'),
    path('sell/', views.SellItemsView.as_view(), name='sell_items'),
    path('', views.ItemListView.as_view(), name='item_list'),
]