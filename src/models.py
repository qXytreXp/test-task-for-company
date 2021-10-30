from peewee import (
    ManyToManyField, 
    Model, 
    PrimaryKeyField, 
    CharField, 
    ForeignKeyField, 
    BooleanField, 
    IntegerField, 
    FloatField, 
    IPField,
    DateTimeField,
)
from src.db import mysql_db


class BaseModel(Model):
    class Meta:
        database = mysql_db


class IpAddressDataThreat(BaseModel):
    is_tor = BooleanField()
    is_proxy = BooleanField()
    is_anonymous = BooleanField()
    is_known_attacker = BooleanField()
    is_known_abuser = BooleanField()
    is_threat = BooleanField()
    is_bogon = BooleanField()


class IpAddressDataTimeZone(BaseModel):
    name = CharField()
    abbr = CharField()
    offset = IntegerField()
    is_dst = BooleanField()
    current_time = DateTimeField()


class IpAddressDataCurrency(BaseModel):
    name = CharField()
    code = CharField(max_length=3)
    symbol = CharField(max_length=1)
    native = CharField(max_length=1)
    plural = CharField()


class IpAddressDataLanguages(BaseModel):
    name = CharField()
    native = CharField()


class IpAddressDataAsn(BaseModel):
    asn = CharField(max_length=55)
    name = CharField(max_length=75)
    domain = CharField()
    route = CharField()
    type = CharField()


class IpAddressData(BaseModel):
    ip = IPField(unique=True)
    is_eu = BooleanField()

    city = CharField()
    region = CharField(max_length=355)
    region_code = IntegerField()

    country_name = CharField()
    country_code = CharField(max_length=5)

    continent_name = CharField()
    continent_code = CharField(max_length=5)

    latitude = FloatField()
    longitude = FloatField()
    postal = IntegerField()
    calling_code = IntegerField()

    flag = CharField(555)
    emoji_flag = CharField(max_length=5)
    emoji_unicode = CharField()

    asn = ForeignKeyField(IpAddressDataAsn, related_name="ipaddressdata", on_delete="CASCADE")
    languages = ManyToManyField(IpAddressDataLanguages, on_delete="CASCADE")
    currency = ForeignKeyField(IpAddressDataCurrency, related_name="ipaddressdata", on_delete="CASCADE")
    time_zone = ForeignKeyField(IpAddressDataTimeZone, related_name="ipaddressdata", on_delete="CASCADE")
    threat = ForeignKeyField(IpAddressDataThreat, related_name="ipaddressdata", on_delete="CASCADE")


class Task(BaseModel):
    id = PrimaryKeyField(null=True)
    celery_task_id = CharField(max_length=36)  # Max celery task id length 36 characters.
    ip_address_data = ForeignKeyField(IpAddressData, related_name="task")


# Task.create_table("task")

# IpAddressDataAsn.create_table("ipaddressdataasn")
# IpAddressDataLanguages.create_table("ipaddressdatalanguages")
# IpAddressDataCurrency.create_table("ipaddressdatacurrency")
# IpAddressDataTimeZone.create_table("ipaddressdatatimezone")
# IpAddressDataThreat.create_table("ipaddressdatathreat")

# IpAddressData.create_table("ipaddressdata")
