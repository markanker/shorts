from ipware import get_client_ip
from hashlib import sha256


def get_hash_ip_address(request):
    ip_address, is_routable = get_client_ip(request)
    hasher = sha256()
    hasher.update(ip_address.encode('utf-8'))
    return hasher.hexdigest()
