# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

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


class WarehouseCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'warehouse_category'


class WarehouseNotification(models.Model):
    is_read = models.BooleanField()
    created_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    message = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'warehouse_notification'


class WarehouseProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    quantity = models.PositiveIntegerField()
    min_quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(WarehouseCategory, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouse_product'


class WarehouseShipment(models.Model):
    date = models.DateTimeField()
    client = models.CharField(max_length=100)
    client_address = models.CharField(max_length=255, blank=True, null=True)
    client_email = models.CharField(max_length=254, blank=True, null=True)
    client_phone = models.CharField(max_length=15, blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    payment_status = models.CharField(max_length=50)
    shipping_method = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'warehouse_shipment'


class WarehouseShipmentitem(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(WarehouseProduct, models.DO_NOTHING)
    shipment = models.ForeignKey(WarehouseShipment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'warehouse_shipmentitem'


class WarehouseSupply(models.Model):
    date = models.DateTimeField()
    supplier = models.CharField(max_length=100)
    created_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouse_supply'


class WarehouseSupplyitem(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(WarehouseProduct, models.DO_NOTHING)
    supply = models.ForeignKey(WarehouseSupply, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'warehouse_supplyitem'
