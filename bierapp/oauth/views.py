from provider.oauth2 import views
from provider.oauth2.models import Grant
from provider.utils import MergeDict

from bierapp.accounts.models import UserMembership
from bierapp.oauth.models import GrantMembership, AccessTokenMembership


class Capture(views.Capture):
    template_name = "oauth2_authorize.html"


class Authorize(views.Authorize):
    template_name = "oauth2_authorize.html"

    def save_authorization(self, request, client, form, client_data):
        code = super(Authorize, self).save_authorization(
            request, client, form, client_data)

        # Grant was created, resolve membership and create a GrantMembership
        if code:
            membership = None
            user = request.user
            grant = Grant.objects.get(
                code=code, client=client, user=user)  # Hack

            # Forced by remote
            request_data = MergeDict(request.GET, request.POST)

            if "site_id" in request_data:
                try:
                    site_id = request_data.get("site_id", 0)
                    membership = UserMembership.objects.get(
                        user=user, site_id=site_id)
                except UserMembership.DoesNotExist:
                    pass

            # Set by login method
            elif hasattr(request, "membership"):
                membership = request.membership

            # Use preferred membership
            else:
                try:
                    membership = UserMembership.objects.filter(
                        user=user).order_by("-is_preferred")[0]
                except IndexError:
                    pass

            # Create companion class that adds membership
            GrantMembership(grant=grant, membership=membership).save()

        return code


class AccessTokenView(views.AccessTokenView):
    def get_authorization_code_grant(self, request, data, client):
        grant = super(AccessTokenView, self).get_authorization_code_grant(
            request, data, client)

        self.membership = GrantMembership.objects.get(grant=grant).membership

        return grant

    def get_refresh_token_grant(self, request, data, client):
        refresh_token = super(AccessTokenView, self).get_refresh_token_grant(
            request, data, client)

        self.membership = AccessTokenMembership.objects.get(
            access_token=refresh_token.access_token).membership

        return refresh_token

    def get_password_grant(self, request, data, client):
        cleaned_data = super(AccessTokenView, self).get_password_grant(
            request, data, client)

        try:
            self.membership = UserMembership.objects.filter(
                user=cleaned_data['user']).order_by("-is_preferred")[0]
        except IndexError:
            pass

        return cleaned_data

    def create_access_token(self, request, user, scope, client):
        access_token = super(AccessTokenView, self).create_access_token(
            request, user, scope, client)

        # Create companion class that adds membership
        AccessTokenMembership(
            access_token=access_token, membership=self.membership).save()

        return access_token

    def invalidate_grant(self, grant):
        if views.constants.DELETE_EXPIRED:
            GrantMembership.objects.filter(grant=grant).delete()

        super(AccessTokenView, self).invalidate_grant(grant)

    def invalidate_access_token(self, access_token):
        if views.constants.DELETE_EXPIRED:
            AccessTokenMembership.objects.filter(
                access_token=access_token).delete()

        super(AccessTokenView, self).invalidate_access_token(access_token)

# Expose views
Redirect = views.Redirect
