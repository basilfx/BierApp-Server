from django.core.management.base import BaseCommand, CommandError

from bierapp.accounts.models import Site

class Command(BaseCommand):
    help = 'Verify sites to have members and/or admin'

    def handle(self, *args, **options):
        sites = Site.objects.select_related().all()

        for site in sites:
            users = [ user for use rin site.members.all() if not user.is_hidden ]

            # Check for members
            if len(users) == 0:
                self.stderr.write("%s: Site is empty" % site)
                continue

            # Check for (non-hidden) admin
            admins = [ user for user in site.members.all() if user.is_admin ]

            if len(admins) == 0:
                self.stderr.write("%s: Site has no (visible) admins." % site)
                continue

