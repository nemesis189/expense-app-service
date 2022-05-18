
from unicodedata import name
from django.urls import include, path, re_path
from . import views
# from views import UserViewSet
# from views import LoginViewSet, RegistrationViewSet, RefreshViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet, basename='users')
# router.register(r'users/<user_email>', views.UsersViewSet.as_view({'get':'list'}), basename='user-email-filter')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'transaction_type', views.TransactionTypeViewSet, basename='transactiontype')
router.register(r'mop', views.ModeOfPaymentViewSet, basename='modeofpayment')
# router.register(r'transactions', views.TransactionsViewSet)
# router.register(r'transact/<int:pk>', views.TransactionsViewSet, basename='transactions_update')
router.register(r'transact', views.TransactionsViewSet, basename='transactions')

router.register(r'login', views.LoginViewSet, basename='auth-login')
router.register(r'register', views.RegistrationViewSet, basename='auth-register')
router.register(r'refresh', views.RefreshViewSet, basename='auth-refresh')

# app_name = 'DB_instance'

urlpatterns = [
    path('myapp/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('transact/<int:pk>', views.TransactionsViewSet.as_view({'put':'partial_update'}), name='transactions_update'),
    path(r'myapp/users/<user_email>', views.UsersViewSet.as_view({'get':'list'}), name='user-email-filter'),
    re_path(r'myapp/transactions-by-user/(?P<user_mail>[a-z0-9]+@[a-z]+\.[a-z]{2,3})/$', views.TrasactionsByUsersListAPIView.as_view(), name='transactions-by-user-detail')
]