from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser admin account'

    def handle(self, *args, **options):
        if not User.objects.filter(email='admin@aiverse.com').exists():
            User.objects.create_superuser(
                email='admin@aiverse.com',
                username='admin',
                full_name='Admin User',
                password='admin123',
                is_admin=True
            )
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
            self.stdout.write(self.style.SUCCESS('Email: admin@aiverse.com'))
            self.stdout.write(self.style.SUCCESS('Password: admin123'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
