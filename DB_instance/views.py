from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer, TransactionTypeSerializer, TransactionsSerializer, UsersSerializer, ModeOfPaymentSerializer
from .models import Category, TransactionType, Transactions, Users, ModeOfPayment
from django.http import HttpResponse, JsonResponse

from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from datetime import datetime, date

# Create your views here.


def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")


class UsersViewSet(viewsets.ModelViewSet):
	queryset = Users.objects.all()
	# print('#######################', list(queryset))
	serializer_class = UsersSerializer

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
	# print('#######################', queryset)
	serializer_class = ModeOfPaymentSerializer


# class TransactionsViewSet1(viewsets.ModelViewSet):
# 	queryset = TransactionType.objects.all()
# 	serializer_class = TransactionsSerializer

	# @action(detail=False, methods=['POST'], name='Create Transaction')
	# def create_transaction(self, request, pk=None, *args, **kwargs):
		# trans = Transactions(tr_id='31', tr_amount=299, tr_date=date.today(), tr_note='Dummy note for dummy transaction', u=1, tr_type=2, mop=3, cat=1)
		# trans = self.get_object()
		# print('################ CREATE TRANS ',request.data)
		# tr_type_serializer = TransactionTypeSerializer(data=request.data)
		# category_serializer = CategorySerializer(data=request.data)
		# tr_type_serializer = TransactionTypeSerializer(data=request.data)
		

		# print('********', date.today())
		# trans.save()
	
class TransactionsViewSet(viewsets.ModelViewSet):
	queryset = Transactions.objects.all()
	serializer_class = TransactionsSerializer

	def create(self, validated_data):
		# print('!!!!!!!!!!!!!! REQUEST',request)
		print('!!!!!!!!!!!!!! VALID', self.request.data)
		# print('!!!!!!!!!!!!!! VALID',JSONParser().parse(self.request.data))0
		# print('!!!!!!!!!!!!!! REQUEST',args, kwargs)
		# return HttpResponse("Hello, world. You're at the Transactions Page.")
		data = validated_data.data
		data1 = {}
	
		print("@@@@@@@@@VALIDATED DATA", data)
		user = data.get('user')[0]
		trans_type = data.get('tr_type')[0]
		mop = data.get('mop')[0]
		category = data.get('category')[0]
		data1["user"] = get_user(user['u_id'], user['u_email']).u_id
		data1["tr_type"] = get_transaction_type(trans_type['tr_type_id'], trans_type['tr_type_name'])
		data1["category"] = get_category(category['cat_id'], category['cat_name'])
		data1["mop"] = get_mop(mop['mop_id'], mop['mop_name'])

		print("TRANSACTIONS  ::::::::: :::::::::::::: ", data1)
		# print("TRANSACTIONS  ::::::::: :::::::::::::: ", **data)
		trans = Transactions.objects.create(**data1)
		
		trans.save()

		return trans


def get_user(u_id, u_email):
	try:
		user = Users.objects.all().filter(u_id=u_id, u_email=u_email)[0]
	except Users.DoesNotExist:
		print ("The User does not exist")
	return user

def get_transaction_type(tr_type_id, tr_type_name):
	print('*&**&*&*&&*&*&*&*&*&*&* TRANS TYPE', tr_type_id, tr_type_name)
	try:
		transaction_type = TransactionType.objects.all().filter(tr_type_id=tr_type_id, tr_type_name=tr_type_name)[0]
		print('*************************************************',transaction_type)
	except TransactionType.DoesNotExist:
		print("The Transaction Type does not exist")
	return transaction_type

def get_category(cat_id, cat_name):
	try:
		category = Category.objects.all().filter(cat_id=cat_id, cat_name=cat_name)[0]
	except Category.DoesNotExist:
		print("The Category does not exist")
	return category

def get_mop(mop_id, mop_name):
	try:
		mop = ModeOfPayment.objects.all().filter(mop_id=mop_id, mop_name=mop_name)[0]
	except Users.DoesNotExist:
		print("The Mode Of Payment does not exist")
	return mop

