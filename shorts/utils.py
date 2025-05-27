from ipware import get_client_ip
from hashlib import sha256


def just_get_ip(request):
    ip_address, _ = get_client_ip(request)
    return ip_address


def get_hash_ip_address(request):
    ip_address = just_get_ip(request)
    hasher = sha256()
    hasher.update(ip_address.encode('utf-8'))
    return hasher.hexdigest()
