from provider.oauth2.views import Authorize, AccessTokenView
from provider.oauth2.forms import AuthorizationForm

from bierapp.accounts.models import UserMembership


class MyAuthorize(Authorize):
    def get_authorization_form(self, request, client, data, client_data):
        instance = MembershipGrant(membership=request.membership)
        return AuthorizationForm(data, instance=instance)


class MyAccessTokenView(AccessTokenView):
    def create_access_token(self, request, user, scope, client,
                            grant=None, access_token=None):

        if grant is not None:
            membership = grant.membership
        elif access_token is not None:
            membership = access_token.membership
        else:
            if "site_id" in request.REQUEST:
                try:
                    site_id = request.REQUEST.get("site_id", 0)
                    membership = UserMembership.objects.get(user=user, site_id=site_id)
                except UserMembership.DoesNotExist:
                    membership = None
            else:
                membership = None

            # Still nothing?
            if membership is None:
                membership = UserMembership.objects.filter(user=user).order_by("-is_preferred")[0]

        # And now?
        if membership is None:
            raise Exception("Cannot continue without a membership.")

        return MembershipAccessToken.objects.create(
            user=user,
            client=client,
            scope=scope,
            membership=membership
        )
