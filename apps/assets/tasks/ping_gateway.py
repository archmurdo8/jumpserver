# ~*~ coding: utf-8 ~*~
from celery import shared_task
from django.utils.translation import gettext_noop

from assets.const import AutomationTypes
from common.utils import get_logger
from orgs.utils import org_aware_func
from .common import quickstart_automation

logger = get_logger(__file__)

__all__ = [
    'test_gateways_connectivity_task',
    'test_gateways_connectivity_manual',
]


@shared_task
@org_aware_func('assets')
def test_gateways_connectivity_task(assets, local_port, task_name=None):
    from assets.models import PingAutomation
    if task_name is None:
        task_name = gettext_noop("Test gateways connectivity ")

    task_name = PingAutomation.generate_unique_name(task_name)
    task_snapshot = {'assets': [str(asset.id) for asset in assets], 'local_port': local_port}
    quickstart_automation(task_name, AutomationTypes.ping_gateway, task_snapshot)


def test_gateways_connectivity_manual(gateway_ids, local_port):
    from assets.models import Asset
    gateways = Asset.objects.filter(id__in=gateway_ids)
    task_name = gettext_noop("Test gateways connectivity ")
    return test_gateways_connectivity_task.delay(gateways, local_port, task_name)
