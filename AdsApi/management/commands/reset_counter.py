# your_app/management/commands/reset_counter.py
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from AdsApi.models import RequestCount

class Command(BaseCommand):
    help = 'Reset the counter value when the next day comes'

    def handle(self, *args, **options):
        # Get the current date
        current_date = datetime.now().date()

        # Check if the counter was last updated on a different date
        count_instance, created = RequestCount.objects.get_or_create(pk=1)
        last_update_date = count_instance.date

        if last_update_date < current_date:
            # Reset the counter value
            count_instance.count = 0
            count_instance.date = current_date
            count_instance.save()

            self.stdout.write(self.style.SUCCESS('Counter reset successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Counter already up to date'))
