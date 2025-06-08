from exceptions import ValidationError
import re
from datetime import datetime as dttm
from django.utils import timezone
from .models import Follower


class FilterValidator:
    pattern_names = r"[a-zа-я]{1}(?:[a-zа-я\-]+)?"
    regex_names = re.compile(pattern_names)

    def __validate_and_set_owner(self, owner: str):
        match owner:
            case 'include':
                self.__owner = True
            case None | 'exclude':
                self.__owner = False
            case _:
                raise ValidationError(f"'owner' parameter must be either 'include', "
                                      f"'exclude', or not provided, but not {owner}")

    def __validate_and_set_device(self, device):
        if device not in ('pc', 'mobile', 'other'):
            raise ValidationError("Device parameter must be either 'pc', 'mobile', or 'other'")
        self.__device = device

    def __validate_and_set_names(self, **names):
        for key, name in names.items():
            if name is not None and not self.regex_names.findall(name):
                raise ValidationError(f"{key} parameter must only contain "
                                      f"lower case letters and '-' chars, but you "
                                      f"provied: {name}")
        for attr, val in names.items():
            setattr(self, f'_{self.__class__.__name__}__{attr}', val)

    def __get_valid_date_or_raise(self, date):
        try:
            y, m, d = map(int, date.split('-'))
        except ValueError:
            raise ValidationError("Wrong date format. The right one is: YYYY-MM-DD")
        try:
            valid_date = dttm(year=y, month=m, day=d)
        except ValueError as ve:
            raise ValidationError(str(ve))
        return timezone.make_aware(valid_date)

    def __validate_and_set_time(self, time, from_time, to_time):
        if not ((time and not (from_time or to_time)) or (not time and from_time)):
            raise ValidationError('You should either set time parameter '
                                  'or time range via from_time and to_time '
                                  'parameters, but not both at the same time. '
                                  'If you want to set a range from some time to now '
                                  'then leave to_time parameter empty')

        if time:
            time = self.__get_valid_date_or_raise(time)
        else:
            from_time = self.__get_valid_date_or_raise(from_time)
            to_time = self.__get_valid_date_or_raise(to_time) if to_time else timezone.now()
            if to_time < from_time:
                raise ValidationError(f"to_time ({to_time}) parameter cannot be earlier "
                                      f"than from_time ({from_time})")

        self.__time, self.__from_time, self.__to_time = time, from_time, to_time

    def __validate_and_set_followers(self, followers):
        match followers:
            case 'all':
                self.__followers = None
            case int() if followers >= 0:
                try:
                    q = Follower.objects.filter(pk=followers)
                    assert q.exists()
                except AssertionError:
                    raise ValidationError(f"There is no such follower with id "
                                          f"you provided ({followers})")
                else:
                    self.__followers = followers
            case int():
                raise ValidationError(f"The follower's id must be a positive number, "
                                      f"not {followers}")
            case _:
                raise ValidationError(f"Followers parameter must be either 'all' "
                                      f"or a positive integer number")

    def __get_db_filter_kwargs(self):
        res = {
            'user_id': self.__user_id,
            'link__short_link': self.__short_link,
            'is_owner': self.__owner,
            'device': self.__device,
            'created_at__date': self.__time,
            'created_at__range': (self.__from_time, self.__to_time) if not self.__time else None,
            'follower__id': self.__followers,
            'follower__country': self.__country,
            'follower__city': self.__city,
            'browser_name': self.__browser,
        }
        return {k: v for k, v in res.items() if v}

    def __init__(self, user_id, short_link=None, owner=None, device='pc', time=None, from_time=None,
                 to_time=None, followers='all', browser=None, country=None, city=None):
        self.__user_id = user_id
        self.__short_link = short_link
        self.__validate_and_set_owner(owner)
        self.__validate_and_set_device(device)
        self.__validate_and_set_time(time, from_time, to_time)
        self.__validate_and_set_followers(followers)
        self.__validate_and_set_names(country=country, city=city, browser=browser)

        self.filter_kwargs = self.__get_db_filter_kwargs()
