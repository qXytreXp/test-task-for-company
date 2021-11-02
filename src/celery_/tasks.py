from ipdata import ipdata

from src.celery_ import app
from src.apps.ipdata_.models import (
    Task,
    IpAddressData,
    Asn, 
    Languages, 
    Currency, 
    TimeZone, 
    Threat 
)


def save_ipdata_response_to_db(response: dict) -> IpAddressData:
    ipdata_model = IpAddressData.create(
        ip=response["ip"],
        is_eu=response["is_eu"],

        city=response["city"],
        region=response["region"],
        region_code=response["region_code"],

        country_name=response["country_name"],
        country_code=response["country_code"],

        continent_name=response["continent_name"],
        continent_code=response["continent_code"],

        latitude=response["latitude"],
        longitude=response["longitude"],
        postal=response["postal"],
        calling_code=response["calling_code"],

        flag=response["flag"],
        emoji_flag=response["emoji_flag"],
        emoji_unicode=response["emoji_unicode"],
    )
    Asn.create(
        ipdata=ipdata_model,
        asn=response["asn"]["asn"],
        name=response["asn"]["name"],
        domain=response["asn"]["domain"],
        route=response["asn"]["route"],
        type=response["asn"]["type"]
    )
    for language in response["languages"]:
        Languages.create(
            ipdata=ipdata_model,
            name=language["name"],
            native=language["native"]
        )
    Currency.create(
        ipdata=ipdata_model,
        name=response["currency"]["name"],
        code=response["currency"]["code"],
        symbol=response["currency"]["symbol"],
        native=response["currency"]["native"],
        plural=response["currency"]["plural"]
    )
    TimeZone.create(
        ipdata=ipdata_model,
        name=response["time_zone"]["name"],
        abbr=response["time_zone"]["abbr"],
        offset=response["time_zone"]["offset"],
        is_dst=response["time_zone"]["is_dst"],
        current_time=response["time_zone"]["current_time"]
    )
    Threat.create(
        ipdata=ipdata_model,
        is_tor=response["threat"]["is_tor"],
        is_proxy=response["threat"]["is_proxy"],
        is_anonymous=response["threat"]["is_anonymous"],
        is_known_attacker=response["threat"]["is_known_attacker"],
        is_known_abuser=response["threat"]["is_known_abuser"],
        is_threat=response["threat"]["is_threat"],
        is_bogon=response["threat"]["is_bogon"]
    )
    return ipdata_model


@app.task
def ipdata_task(ip: str, task_model_id: int) -> None:
    """ Get data about ip address and save to db """
    ipdata_ = ipdata.IPData("d59525ba98387b087900982d2f8beb33f6d640eeac7437b12e3c0b68")
    response = ipdata_.lookup(ip)
    ipdata_model = save_ipdata_response_to_db(response)

    task_model = Task.get(Task.id == task_model_id)
    task_model.ipdata = ipdata_model
    task_model.save()
