import secrets
from urllib.parse import urlparse
import ipaddress
import socket

def generate_token(length=8):
    return secrets.token_urlsafe(length)[:length]

from urllib.parse import urlparse
import ipaddress
import socket

def is_valid_url(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False

        host = parsed.hostname

        ip = socket.gethostbyname(host)

        ip_obj = ipaddress.ip_address(ip)

        if (
            ip_obj.is_private or
            ip_obj.is_loopback or
            ip_obj.is_reserved
        ):
            return False

        return True
    
    except:
        return False