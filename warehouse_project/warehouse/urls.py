from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),

    path('add_numbers/', views.add_numbers, name='add_numbers'),
    path('task_status/<str:task_id>/', views.task_status, name='task_status'),

    path('products/', views.products, name='products'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),

    path('supplies/', views.supplies, name='supplies'),
    path('supplies/<int:pk>/', views.supply_detail, name='supply_detail'),
    path('supplies/delete/<int:pk>/', views.delete_supply, name='delete_supply'),

    path('shipments/', views.shipments, name='shipments'),
    path('shipments/<int:pk>/', views.shipment_detail, name='shipment_detail'),
    path('shipments/delete/<int:pk>/', views.delete_shipment, name='delete_shipment'),

    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/read/<int:notif_id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/delete/<int:notif_id>/', views.delete_notification, name='delete_notification'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]