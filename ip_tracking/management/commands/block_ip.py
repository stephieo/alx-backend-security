from django.core.management.base import BaseCommand
from ip_tracking.models import RequestLog, BlockedIP

class Command(BaseCommand):
    help: " this adds an IP address to a blacklist db"

    def add_arguments(self, parser):
        ''' the optional and required args for this command'''
        parser.add_argument('ip_address', type=str, help='the IP address you want to block')

    def handle(self, *args, **options):
        ip = options['ip_address']
        BlockedIP.objects.create(ip_address=ip)
        self.stdout.write(self.style.SUCCESS(f'IP: {ip} -- added to blacklist'))