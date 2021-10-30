from ipdata import ipdata
from src.celery_ import celery_app
from src.models import IpAddressData


def save_ip_address_data(data: dict) -> None:
    data = IpAddressData.create(**data)
    print(data.ip)


@celery_app.task
def get_ip_data_task(ip: str) -> dict:
    ipdata_ = ipdata.IPData("d59525ba98387b087900982d2f8beb33f6d640eeac7437b12e3c0b68")
    response = ipdata_.lookup(ip)
    save_ip_address_data(response)

    return dict(response)


# from celery.result import AsyncResult

# result = AsyncResult("task-id", app=celery_app)
# print(result.get())
