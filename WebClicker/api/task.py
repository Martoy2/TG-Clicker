from celery import shared_task
from main.models import Pool


@shared_task
def update_ticket():
    pool_instance = Pool.objects.get(pool_name='Main')
    pool_instance.ticket += pool_instance.z
    pool_instance.save()