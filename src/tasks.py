from ipdata import ipdata
from src.celery_ import celery_app
from src.models import Task, IpAddressData, IpAddressDataAsn, IpAddressDataLanguages, IpAddressDataCurrency, IpAddressDataTimeZone, IpAddressDataThreat


def save_ip_address_data(data: dict) -> None:
    asn = IpAddressDataAsn.create(
        asn=data["asn"]["asn"],
        name=data["asn"]["name"],
        domain=data["asn"]["domain"],
        route=data["asn"]["route"],
        type=data["asn"]["type"]
    ).get()

    currency = IpAddressDataCurrency.create(
        name=data["currency"]["name"],
        code=data["currency"]["code"],
        symbol=data["currency"]["symbol"],
        native=data["currency"]["native"],
        plural=data["currency"]["plural"]
    ).get()

    time_zone = IpAddressDataTimeZone.create(
        name=data["time_zone"]["name"],
        abbr=data["time_zone"]["abbr"],
        offset=data["time_zone"]["offset"],
        is_dst=data["time_zone"]["is_dst"],
        current_time=data["time_zone"]["current_time"]
    ).get()

    threat = IpAddressDataThreat.create(
        is_tor=data["threat"]["is_tor"],
        is_proxy=data["threat"]["is_proxy"],
        is_anonymous=data["threat"]["is_anonymous"],
        is_known_attacker=data["threat"]["is_known_attacker"],
        is_known_abuser=data["threat"]["is_known_abuser"],
        is_threat=data["threat"]["is_threat"],
        is_bogon=data["threat"]["is_bogon"]
    ).get()

    ipaddrsdata = IpAddressData(
        ip=data["ip"],
        is_eu=data["is_eu"],

        city=data["city"],
        region=data["region"],
        region_code=data["region_code"],

        country_name=data["country_name"],
        country_code=data["country_code"],

        continent_name=data["continent_name"],
        continent_code=data["continent_code"],

        latitude=data["latitude"],
        longitude=data["longitude"],
        postal=data["postal"],
        calling_code=data["calling_code"],

        flag=data["flag"],
        emoji_flag=data["emoji_flag"],
        emoji_unicode=data["emoji_unicode"],

        asn=asn,
        currency=currency,
        time_zone=time_zone,
        threat=threat
    )
    for language in data["languages"]:
        ipaddrsdata.languages.add(IpAddressDataLanguages.create(
            name=language["name"],
            native=language["native"]
        ))
    print(f"##### {ipaddrsdata.ip}")
    ipaddrsdata.save()

    return ipaddrsdata


@celery_app.task
def get_ip_data_task(ip: str) -> dict:
    ipdata_ = ipdata.IPData("d59525ba98387b087900982d2f8beb33f6d640eeac7437b12e3c0b68")
    response = ipdata_.lookup(ip)
    # save_ip_address_data(response, model_task_id)

    return dict(response)


# from celery.result import AsyncResult

# result = AsyncResult("task-id", app=celery_app)
# print(result.get())
