from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer, TransactionTypeSerializer, TransactionsSerializer, UsersSerializer, ModeOfPaymentSerializer
# from .serializers import  TransactionTypeSerializer, TransactionsSerializer, UsersSerializer, ModeOfPaymentSerializer
# from .models import  TransactionType, Transactions, Users, ModeOfPayment
from .models import Category, TransactionType, Transactions, Users, ModeOfPayment
from django.http import HttpResponse, JsonResponse

from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from datetime import datetime, date

from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.
# curl -H "Authorization: Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5NzQ3NzE4LCJpYXQiOjE2NDk3NDc0MTgsImp0aSI6ImIzOGZiZTQ5MTQxMzRhMDk4MmZkYTNjMzA5MmQ2NjY3IiwidXNlcl9pZCI6MX0.LDXr_wYwWD8EPQdAHCnBN1fDGV_dy-mGpPdwEOPOln8"  http://127.0.0.1:8000/myapp/users/ 

def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")


class UsersViewSet(viewsets.ModelViewSet):
	queryset = Users.objects.all()
	# print('#######################', list(queryset))
	serializer_class = UsersSerializer
	# authentication_classes = (TokenAuthentication,) 
	permission_classes = (IsAuthenticated,)

	def get_object(self):
		lookup_field_value = self.kwargs[self.lookup_field]
		print("LOOKUP FIELD VALUE", lookup_field_value)
		obj = Users.objects.get(lookup_field_value)
		self.check_object_permissions(self.request, obj)

		return obj

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	# print('#######################', list(queryset))
	serializer_class = CategorySerializer


class TransactionTypeViewSet(viewsets.ModelViewSet):
	queryset = TransactionType.objects.all()
	# print('#######################', queryset)
	serializer_class = TransactionTypeSerializer

class ModeOfPaymentViewSet(viewsets.ModelViewSet):
	queryset = ModeOfPayment.objects.all()
	serializer_class = ModeOfPaymentSerializer
	
class TransactionsViewSet(viewsets.ModelViewSet):
	queryset = Transactions.objects.all()
	serializer_class = TransactionsSerializer
	http_method_names = ['get', 'post', 'put', 'patch', 'delete']

	def create(self, request, *args, **kwargs):
		data = request.data
		user_email = (request.data).pop('u')
		user = Users.objects.get(u_email=user_email)

		serialized_user = UsersSerializer(user, context={'request': request})
		data['u'] = (serialized_user.data).get("url")
		print('DATA AAAAAAAAAAAaaa',data, type(data))
		serializer = TransactionsSerializer(data=data, context={'request': request})
		serializer.is_valid()
		print(serializer.is_valid())
		print(serializer.errors)
		self.perform_create(serializer)
		print("TRANS VIEW ", serializer.data, data, user)
		return Response({
            'transactions': serializer.data
        })

	def update(self, request, pk=None, *args, **kwargs):
		data = request.data
		user_email = (request.data).pop('u')
		user = Users.objects.get(u_email=user_email)

		serialized_user = UsersSerializer(user, context={'request': request})
		data['u'] = (serialized_user.data).get("url")
		print('UPDATEEEEEEEEEEEE  DATA AAAAAAAAAAAaaa',data, type(data))


		partial = True # Here I change partial to True
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		
		return Response(serializer.data)


class TrasactionsByUsersListAPIView(generics.ListAPIView):
	serializer_class = TransactionsSerializer
	http_method_names = ['get']

	def get(self, request, user_mail, *args, **kwargs):
		print("KWARGSSSSS", kwargs)
		user = Users.objects.get(u_email=user_mail)
		serialized_transactions = list(
			Transactions.objects.filter(u=user).values(
				'tr_id',
				'u__u_email',
				'cat__cat_name', 
				'mop__mop_name',
				'tr_type__tr_type_name',
				'tr_amount', 
				'tr_date',
				'tr_note',
			).order_by('-tr_date')
		)

		yearlyMonthlyTransactions = getYearlyMonthlyTransactions(serialized_transactions)
		
		print('YEARLY MONTHLY TRANS :::::::::::::::::: ', yearlyMonthlyTransactions)
		return Response({
            'transactions': serialized_transactions,
			'ordered_by_time_period': yearlyMonthlyTransactions
        })


class LoginViewSet(viewsets.ModelViewSet, TokenObtainPairView):
	serializer_class = LoginSerializer
	permission_classes = (AllowAny,)
	http_method_names = ['post']

	def create(self, request, *args, **kwargs):
		serializer_context = {'request': request,}
		print("LOGIN VIEWSET CONTEXT", serializer_context)
		serializer = self.get_serializer(data=request.data, context=serializer_context)

		try:
			serializer.is_valid(raise_exception=True)
		except TokenError as e:
			raise InvalidToken(e.args[0])

		return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(viewsets.ModelViewSet, TokenObtainPairView):
	serializer_class = RegisterSerializer
	permission_classes = (AllowAny,)
	http_method_names = ['post']

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		refresh = RefreshToken.for_user(user)
		res = {
			"refresh": str(refresh),
			"access": str(refresh.access_token),
		}

		return Response({
			"user": serializer.data,
			"refresh": res["refresh"],
			"token": res["access"]
		}, status=status.HTTP_201_CREATED)


class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
	permission_classes = (AllowAny,)
	http_method_names = ['post']

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		try:
			serializer.is_valid(raise_exception=True)
		except TokenError as e:
			raise InvalidToken(e.args[0])

		return Response(serializer.validated_data, status=status.HTTP_200_OK)



def getYearlyMonthlyTransactions(transactions):

	def get_key(t, year):
		k = str(t['tr_date'].year) if year else str(t['tr_date'].month)
		return '_'+ k


	sortedDict = {}

	# Sorting in to dictionaries of years
	for t in transactions:
		if get_key(t, True) in sortedDict.keys():
			sortedDict[get_key(t, True)].append(t)
		else:
			sortedDict[get_key(t, True)] = [t]

	# Sorting by months within years
	finalSorted = {}
	for year,yearlyTrans in sortedDict.items():
		if year not in finalSorted:
			finalSorted[year] = {}
		sortedByMonth = {}
		for t in yearlyTrans:
			if get_key(t, False) not in sortedByMonth.keys():
				sortedByMonth[get_key(t, False)] = [t]
			else:
				sortedByMonth[get_key(t, False)].append(t)
		
		finalSorted[year] = sortedByMonth
	# print("FINAL SORTED HEREHERE HERE ::::::::::::::::::;;", finalSorted)
	return [finalSorted]




