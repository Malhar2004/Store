from django.http import HttpRequest

## get IP address
def get_client_ip(request: HttpRequest) -> str:
    """
    Extracts the client's IP address from the request headers.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip