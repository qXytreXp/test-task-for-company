from peewee import (
    Model, 
    CharField, 
    ForeignKeyField, 
    BooleanField, 
    IntegerField, 
    FloatField, 
    IPField,
    DateTimeField
)
from src.db import mysql_db


class BaseModel(Model):
    class Meta:
        database = mysql_db


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


class Asn(BaseModel):
    ipdata = ForeignKeyField(IpAddressData, backref="asn", unique=True)
    name = CharField(max_length=75)
    domain = CharField()
    route = CharField()
    type = CharField()


class Threat(BaseModel):
    ipdata = ForeignKeyField(IpAddressData, backref="threat", unique=True)
    is_tor = BooleanField()
    is_proxy = BooleanField()
    is_anonymous = BooleanField()
    is_known_attacker = BooleanField()
    is_known_abuser = BooleanField()
    is_threat = BooleanField()
    is_bogon = BooleanField()


class TimeZone(BaseModel):
    ipdata = ForeignKeyField(IpAddressData, backref="time_zone", unique=True)
    name = CharField()
    abbr = CharField()
    offset = IntegerField()
    is_dst = BooleanField()
    current_time = DateTimeField()


class Currency(BaseModel):
    ipdata = ForeignKeyField(IpAddressData, backref="currency", unique=True)
    name = CharField()
    code = CharField(max_length=3)
    symbol = CharField(max_length=1)
    native = CharField(max_length=1)
    plural = CharField()


class Languages(BaseModel):
    ipdata = ForeignKeyField(IpAddressData, backref="languages")
    name = CharField()
    native = CharField()


class Task(BaseModel):
    ipdata = ForeignKeyField(IpAddressData, backref="task", unique=True, null=True)
    celery_task_id = CharField(max_length=36, null=True)
