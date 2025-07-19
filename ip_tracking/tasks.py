from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP
@shared_task
def detect_anomalies():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    sensitive_paths = ['/admin', '/login']
    ip_counts = RequestLog.objects.filter(timestamp__gte=one_hour_ago) \
        .values('ip_address') \
        .annotate(count=models.Count('id')) \
        .filter(count__gt=100)
    for ip_data in ip_counts:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip_data['ip_address'],
            defaults={'reason': f"Exceeded 100 requests/hour: {ip_data['count']}"}
        )
    sensitive_requests = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address').distinct()
    for req in sensitive_requests:
        SuspiciousIP.objects.get_or_create(
            ip_address=req['ip_address'],
            defaults={'reason': 'Accessed sensitive path'}
        )