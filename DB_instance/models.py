from django.db import models

# Create your models here.


class Category(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    cat_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'Category'


class ModeOfPayment(models.Model):
    mop_id = models.IntegerField(primary_key=True)
    mop_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'Mode Of Payment'


class TransactionType(models.Model):
    tr_type_id = models.IntegerField(primary_key=True)
    tr_type_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'Transaction Type'


class Transactions(models.Model):
    tr_id = models.IntegerField(primary_key=True)
    tr_amount = models.FloatField()
    tr_date = models.DateField()
    tr_note = models.TextField(blank=True, null=True)
    u = models.ForeignKey('Users', models.DO_NOTHING, related_name='user')
    tr_type = models.ForeignKey(TransactionType, models.DO_NOTHING, related_name='tr_type')
    mop = models.ForeignKey(
        ModeOfPayment, models.DO_NOTHING, blank=True, null=True, related_name='mop')
    cat = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True, related_name='category')

    class Meta:
        managed = False
        db_table = 'Transactions'


class Users(models.Model):
    u_id = models.IntegerField(primary_key=True)
    u_name = models.TextField()
    u_email = models.TextField()
    u_password = models.TextField()
    u_creation_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'Users'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
