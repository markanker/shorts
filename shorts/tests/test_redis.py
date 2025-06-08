from django.core.cache import cache as redis_cache
from time import sleep
import pytest


def test_redis_basic_availability():
    redis_cache.set('k1', 'v1', -1)
    assert redis_cache.get('k1') == 'v1'
    assert redis_cache.delete('k1')
    redis_cache.set('k2', 'v2', 1)
    sleep(1.2)
    assert redis_cache.get('k2') == 'v2'
    redis_cache.set_many({'k3': 'v3', 'k4': 'v4'})
    assert redis_cache.delete_many(['k2', 'k3', 'k4'])
    redis_cache.set('k5', 'v5')
    redis_cache.clear()
    assert not redis_cache.get('k5')
