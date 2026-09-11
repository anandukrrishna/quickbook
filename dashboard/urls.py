from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/add/', views.add_vendor, name='add_vendor'),
    path('vendors/<int:vendor_id>/edit/',views.edit_vendor,name='edit_vendor'),
    path('vendors/<int:vendor_id>/delete/',views.delete_vendor,name='delete_vendor'),
    path('events/',views.event_list,name='event_list'),
    path('events/add/',views.add_event,name='add_event'),
    path('events/<int:event_id>/edit/',views.edit_event,name='edit_event'),
    path('events/<int:event_id>/delete/',views.delete_event,name='delete_event'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/',views.user_detail,name='user_detail'),

]