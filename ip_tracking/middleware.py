from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.core.cache import cache
from ipgeolocation import ipgeolocation
from .models import RequestLog, BlockedIP

class IPLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = self.get_client_ip(request)
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden()
        path = request.path
        RequestLog.objects.create(ip_address=ip, path=path)
        return None

    