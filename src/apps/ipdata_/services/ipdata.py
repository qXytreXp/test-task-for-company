from src.celery_.tasks import ipdata_task

from src.apps.ipdata_.models import (
    Task, 
    IpAddressData
)


def create_task_for_getting_data_about_ip(ip: str) -> Task:
    task_model = Task.create()

    celery_task = ipdata_task.delay(ip=ip, task_model_id=task_model.id)

    task_model.celery_task_id = celery_task.id
    task_model.save()

    return task_model


def ipaddrs_exists_in_db(ip: str) -> bool:
    try:
        IpAddressData.get(IpAddressData.ip == ip)
        return True
    except IpAddressData.DoesNotExist:
        return False


def get_task_model_by_ipdata_ip(ip: str) -> Task:
    ipdata_model = IpAddressData.get(IpAddressData.ip == ip)
    task_model = Task.get(Task.ipdata == ipdata_model)
    return task_model


def get_task_model_by_id(task_id: int) -> Task:
    return Task.get(Task.id == task_id)
