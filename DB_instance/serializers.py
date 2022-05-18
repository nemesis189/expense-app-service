from rest_framework import serializers
# from .models import ModeOfPayment, TransactionType, Transactions, Users
from .models import Category, ModeOfPayment, TransactionType, Transactions, Users
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist


class UsersSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="users-detail")
	class Meta:
		model = Users
		# fields = ['u_id', 'u_name', 'u_email', 'u_password', 'u_creation_date']
		# extra_kwargs = {'view_name': 'DB_instance:users-detail'}
		fields = '__all__'
		# exclude = ['url']

class LoginSerializer(TokenObtainPairSerializer):
	model = Users
	def validate(self, attrs):
		user = self.model.objects.get(u_email=attrs['username'], u_password=attrs['password'])
		if not user:
			print('User Not Found')
		context = self.context
		print("CONTEXTTTT",)
		user_data = UsersSerializer(user, context=context).data
		refresh = self.get_token(user) 
		data = dict()
		data['user'] = user_data
		data['refresh'] = str(refresh)
		data['access'] = str(refresh.access_token)

		if api_settings.UPDATE_LAST_LOGIN:
			update_last_login(None, user)

		return data

class RegisterSerializer(UsersSerializer):
	class Meta:
		model = Users
		# fields = ['u_id', 'u_name', 'u_email', 'u_password', 'u_creation_date']
		fields = '__all__'
		# fields = ['id', 'username', 'email', 'password', 'is_active', 'created', 'updated']

	def create(self, validated_data):
		print("REGISTER SERIAL $$$$$$$$$$$$$$$$$$", validated_data)
		try:
			user = Users.objects.get(u_email=validated_data['u_email'])
		except :
			print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$', validated_data )
			user = Users.objects.create(**validated_data)
		
		return user


class CategorySerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="category-detail")
	class Meta:
		model = Category
		# fields = ['cat_id', 'cat_name']
		# extra_kwargs = {'view_name': 'DB_instance:category-detail'}
		fields = '__all__'


class ModeOfPaymentSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="modeofpayment-detail")
	class Meta:
		model = ModeOfPayment
		# fields = ['mop_id', 'mop_name']
		# extra_kwargs = {'view_name': 'DB_instance:modeofpayment-detail'}
		fields = '__all__'


class TransactionTypeSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="transactiontype-detail")
	class Meta:
		model = TransactionType
		# extra_kwargs = {'view_name': 'DB_instance:transaction_type-detail'}
		# fields = ['tr_type_id', 'tr_type_name']
		fields = '__all__'
		# exclude = ['url']


class TransactionsSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Transactions
		# fields = ['tr_id', 'tr_amount', 'tr_date', 'tr_note', 'u', 'tr_type', 'mop', 'cat']
		fields = '__all__'
		# exclude = ['url']
		print("WILL CREATE TRANSACTION ********************************* ")

	def create(self, validated_data):
		print("WILL CREATE TRANSACTION ", validated_data)
		transaction = Transactions.objects.create(**validated_data)
		print("CREATED TRANSACTION ", transaction)
		return transaction
	
	def update(self, instance, validated_data):
		instance.u = validated_data.get('u')
		instance.tr_amount = validated_data.get('tr_amount')
		instance.tr_date = validated_data.get('tr_date')
		instance.tr_note = validated_data.get('tr_note')
		instance.cat = validated_data.get('cat')
		instance.mop = validated_data.get('mop')
		instance.save()
		return instance
		