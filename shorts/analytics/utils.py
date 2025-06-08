from .models import LinkStats, Follower
from datetime import timedelta
from django.utils import timezone
from utils import just_get_ip
import requests

from django.conf import settings
data_by_ip = settings.DATA_BY_IP_SERVICE
data_from_ua = settings.DATA_FROM_USER_AGENT_SERVICE


def obtain_follower(request):
    ip_address = just_get_ip(request)

    endpoint = f'{data_by_ip['url_root_pattern']}{ip_address}'
    service_response = requests.get(endpoint, params={'token': data_by_ip['api_key']}).json()

    country = service_response['country']
    city = service_response['city']
    region = service_response['region']

    return Follower.objects.get_or_create(
        ip_address=ip_address,
        country=country,
        city=city,
        region=region,
    )[0]


def analytics_mark_in(request, link):
    is_owner = request.user == link.user
    if is_owner:
        follower = None
    else:
        follower = obtain_follower(request)
    if len((last_visit := LinkStats.objects.filter(
        link=link, follower=follower, is_owner=is_owner
    ))) > 0:
        if timezone.now() - last_visit.last().created_at < timedelta(minutes=5):
            return None

    user_agent = request.META['HTTP_USER_AGENT']

    endpoint = f'{data_from_ua['url_root_pattern']}'
    service_response = requests.get(endpoint, params={'ua': user_agent, 'key': 'NOTREQUIED'}).json()

    device = service_response['device']['deviceType']
    device = 'pc' if device == 'desktop' else device
    browser_name = service_response['browser']['name']
    os_name = service_response['os']['name']
    os_version = service_response['os']['version']

    LinkStats.objects.create(
        link=link,
        follower=follower,
        user_id=request.user.pk,
        is_owner=is_owner,
        device=device,
        browser_name=browser_name,
        os_name=os_name,
        os_version=os_version,
    )
