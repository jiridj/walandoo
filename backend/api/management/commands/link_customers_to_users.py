from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Customer

class Command(BaseCommand):
    help = 'Link existing Customer records to User accounts by email (creates users if needed)'

    def handle(self, *args, **options):
        for customer in Customer.objects.filter(user__isnull=True):
            user, created = User.objects.get_or_create(
                username=customer.email,
                defaults={
                    'email': customer.email,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'is_active': True,
                }
            )
            customer.user = user
            customer.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created user for customer {customer.email}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Linked customer {customer.email} to existing user'))
        self.stdout.write(self.style.SUCCESS('All customers linked to users.'))
