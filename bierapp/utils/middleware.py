from django.utils.deprecation import MiddlewareMixin

from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header

from provider.oauth2.models import AccessToken

from bierapp.accounts.models import UserMembership, UserMembershipInvite
from bierapp.oauth.models import AccessTokenMembership


class OAuth2MiddlewareRequest(MiddlewareMixin):
    def process_request(self, request):
        auth_header = get_authorization_header(request)

        # Grab access token.
        if not auth_header:
            return

        # Strip access token.
        auth = auth_header.decode("ascii").split(" ")

        if len(auth) != 2:
            request.oauth2_exception = exceptions.ParseError()
            return

        # Retrieve token from the database.
        try:
            access_token = AccessToken.objects \
                .select_related("user") \
                .get(token=auth[1])
        except AccessToken.DoesNotExist:
            request.oauth2_exception = exceptions.AuthenticationFailed()
            return

        # Check expire time.
        if access_token.get_expire_delta() < 0:
            request.oauth2_exception = exceptions.AuthenticationFailed()
            return

        # Check for user to be active.
        if not access_token.user.is_active:
            request.oauth2_exception = exceptions.PermissionDenied()
            return

        # Resolve membership.
        try:
            access_token_membership = AccessTokenMembership.objects \
                .select_related("membership", "membership__site") \
                .get(access_token=access_token)
        except AccessTokenMembership.DoesNotExist:
            access_token_membership = None

        # Set required properties.
        request.oauth2_token = access_token
        request.user = request._user = access_token.user

        if access_token_membership:
            request.membership = access_token_membership.membership
            request.site = access_token_membership.membership.site


class SiteMiddlewareRequest(MiddlewareMixin):
    def process_request(self, request):
        """
        Make the current site available in the parameter "request.membership".
        The first attempt tries to use the "membership_id" from the current
        session. If no id is set, it tries to query the first preferred site.

        If the user does not have any sites, or the user is not authenticated,
        the parameter "request.membership" will not exist.
        """

        # Don't do the same thing twice
        if hasattr(request, "membership"):
            return

        if request.user.is_authenticated():
            membership_id = request.session.get("membership_id", False)

            try:
                request.membership = UserMembership.objects.select_related(
                    "site").get(pk=membership_id, user=request.user)
            except UserMembership.DoesNotExist:
                try:
                    request.membership = UserMembership.objects.select_related(
                        "site").filter(
                            user=request.user).order_by("-is_preferred")[0]

                    # Update session so it does not cost two queries next time
                    if membership_id != request.membership.id:
                        request.session["membership_id"] = \
                            request.membership.id
                except IndexError:
                    pass

            # Required to stay compatible with API, where memberships may not
            # be applicable
            if hasattr(request, "membership"):
                request.site = request.membership.site
            else:
                request.site = None

            # Show pending membership invites
            request.membership_invites = UserMembershipInvite.objects.filter(
                email=request.user.email)
