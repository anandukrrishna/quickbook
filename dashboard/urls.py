from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/add/', views.add_vendor, name='add_vendor'),
    path('vendors/<int:vendor_id>/edit/',views.edit_vendor,name='edit_vendor'),
    path('vendors/<int:vendor_id>/delete/',views.delete_vendor,name='delete_vendor'),

]