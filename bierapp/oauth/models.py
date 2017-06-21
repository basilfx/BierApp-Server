from django.db import models


class GrantMembership(models.Model):
    grant = models.OneToOneField("oauth2.Grant")
    membership = models.ForeignKey("accounts.UserMembership", null=True)


class AccessTokenMembership(models.Model):
    access_token = models.OneToOneField("oauth2.AccessToken")
    membership = models.ForeignKey("accounts.UserMembership", null=True)
