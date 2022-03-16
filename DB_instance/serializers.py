from rest_framework import serializers
from .models import Category, ModeOfPayment, TransactionType, Transactions, Users


class UsersSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Users
		fields = ['u_id', 'u_name', 'u_email', 'u_password', 'u_creation_date']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Category
		fields = ['cat_id', 'cat_name']


class ModeOfPaymentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ModeOfPayment
		fields = ['mop_id', 'mop_name']


class TransactionTypeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = TransactionType
		fields = ['tr_type_id', 'tr_type_name']

class TransactionsSerializer(serializers.HyperlinkedModelSerializer):
	user = UsersSerializer()
	tr_type = TransactionTypeSerializer()
	mop = ModeOfPaymentSerializer()
	category = CategorySerializer()
	class Meta:
		model = Transactions
		fields = ['tr_id', 'tr_amount', 'tr_date', 'tr_note', 'user', 'tr_type', 'mop', 'category']
		# fields = '__all__'

# class TransactionsSerializer111(serializers.HyperlinkedModelSerializer):
	# u_id = UsersSerializer()
	# user = UsersSerializer()
	# tr_type = CategorySerializer()
	# mop = ModeOfPaymentSerializer()
	# category = CategorySerializer()
	# class Meta:
		# model = Transactions
		# fields = ['tr_id', 'tr_amount', 'tr_date', 'tr_note', 'user', 'tr_type', 'mop', 'category']
		# fields = ['tr_id', 'tr_amount', 'tr_date', 'tr_note', 'category']
		# fields='__all__'
	
	

