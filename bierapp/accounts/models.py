from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _, ugettext as __

from django_extensions.db.models import TimeStampedModel

from custom_user.models import AbstractEmailUser, EmailUserManager

import uuid

ROLE_ADMIN = 1
ROLE_MEMBER = 2
ROLE_GUEST = 3


class UserManager(EmailUserManager):
    """
    """

    use_for_related_fields = True

    def members(self):
        return self.get_queryset().filter(
            memberships__role__in=[ROLE_ADMIN, ROLE_GUEST])

    def guests(self):
        return self.get_queryset().filter(
            memberships__role__in=[ROLE_GUEST])

    def active(self):
        return self.get_queryset().filter(memberships__is_hidden=False)

    def inactive(self):
        return self.get_queryset().filter(memberships__is_hidden=True)


class User(TimeStampedModel, AbstractEmailUser):
    """
    """

    first_name = models.CharField(_("first name"), max_length=128, blank=False)
    last_name = models.CharField(_("last name"), max_length=128, blank=False)

    birthdate = models.DateField(null=True)

    avatar = models.ImageField(
        width_field="avatar_width", height_field="avatar_height",
        upload_to=lambda x, y: "avatars/%d_%s" % (x.id, y), null=True)
    avatar_width = models.PositiveIntegerField(null=True)
    avatar_height = models.PositiveIntegerField(null=True)

    is_deleted = models.BooleanField(default=False, null=False)

    objects = UserManager()

    def __unicode__(self):
        """
        Simple to string which renders first name and last name.
        """

        return self.get_full_name() or unicode()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """

        if self.first_name and self.last_name:
            return ("%s %s" % (self.first_name, self.last_name)).strip()
        else:
            return self.get_short_name()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """

        if self.first_name:
            return self.first_name
        else:
            return __("Nameless")


class UserMembershipInvite(TimeStampedModel, models.Model):
    """
    """

    site = models.ForeignKey("Site", related_name="membership_invites")

    email = models.EmailField(null=False, blank=False)
    token = models.CharField(max_length=128, null=False, blank=False)
    role = models.PositiveIntegerField(default=ROLE_MEMBER, null=False)

    class Meta:
        unique_together = (("site", "email"), )

    def __unicode__(self):
        return u"%s -> %s (%s)" % (self.site, self.email, self.token)

    def save(self, *args, **kwargs):
        # Generate unique token if empty
        if not self.token:
            self.token = uuid.uuid4().hex

        # Save
        return super(UserMembershipInvite, self).save(*args, **kwargs)


class UserMembership(TimeStampedModel, models.Model):
    """
    """

    site = models.ForeignKey("Site", related_name="memberships")
    user = models.ForeignKey("User", related_name="memberships")

    position = models.PositiveIntegerField(default=1, null=False)
    role = models.PositiveIntegerField(default=ROLE_MEMBER, null=False)

    is_hidden = models.BooleanField(default=False, null=False)
    is_preferred = models.BooleanField(default=False, null=False)

    class Meta:
        ordering = ("position",)
        unique_together = (("user", "site"), )

    def __unicode__(self):
        return u"%s -> %s" % (self.user, self.site)

    @property
    def is_admin(self):
        return self.role in [ROLE_ADMIN]

    @property
    def is_guest(self):
        return self.role in [ROLE_GUEST]

    @property
    def is_member(self):
        return self.role in [ROLE_ADMIN, ROLE_MEMBER]


class Site(TimeStampedModel, models.Model):
    """
    """

    name = models.CharField(max_length=100)
    users = models.ManyToManyField(
        "User", through="UserMembership", related_name="sites")

    objects = models.Manager()
    api_objects = models.Manager()

    class Meta:
        ordering = ("name", )

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return reverse("bierapp.accounts.views.site", kwargs={"id": self.id})
