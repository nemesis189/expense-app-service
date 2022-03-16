
from unicodedata import name
from django.urls import include, path
from . import views

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'transaction_type', views.TransactionTypeViewSet)
router.register(r'mop', views.ModeOfPaymentViewSet)
router.register(r'transactions', views.TransactionsViewSet)
router.register(r'transact', views.TransactionsViewSet)

# app_name = 'DB_instance'

urlpatterns = [
    path('myapp/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
