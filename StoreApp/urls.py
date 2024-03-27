from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('form', views.CustomerInfo, basename="CustomerInfo")

router1 = DefaultRouter()
router1.register('drdate', views.DrawDate, basename="DrawDate")

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('user/', views.get_user_info, name='user_info'),
    path('delexp/', views.export_deleted_to_excel, name="deleted_record_to_excel"),
    path('exp/', views.export_to_excel, name= 'exp_excel'),
    path('date/', include(router1.urls)),
    path('delrecord/<int:record_id>/', views.soft_delete_record, name="soft_delete_record"),
    path('delrecord/', views.list_deleted_records, name="list_deleted_record")
]

