from .models import LinkStats, Follower
from datetime import datetime, timedelta, timezone
from utils import just_get_ip


def obtain_follower(request):
    ip_address = just_get_ip(request)
    country = ...
    city = ...
    return Follower.objects.get_or_create(
        ip_address=ip_address,
        country=country,
        city=city
    )


def analytics_mark_in(request, link):
    is_owner = request.user == link.user
    if is_owner:
        follower = None
    else:
        follower = obtain_follower(request)
    if len((last_visit := LinkStats.objects.filter(
        link=link, follower=follower, is_owner=is_owner
    ))) > 0:
        if datetime.now(timezone.utc) - last_visit.last().created_at < timedelta(minutes=5):
            return None

    device, browser_name = ..., ...

    LinkStats.objects.create(
        link=link,
        follower=follower,
        is_owner=is_owner,
        device=device,
        browser_name=browser_name,
    )
