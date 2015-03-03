from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, \
    logout as auth_logout
from django.contrib import messages

from bierapp.accounts.models import User, UserMembershipInvite, \
    UserMembership, ROLE_ADMIN, ROLE_MEMBER, ROLE_GUEST
from bierapp.accounts.forms import RegisterForm, UserMembershipInviteForm, \
    SiteForm, ChangeProfileForm, AuthenticationForm, ChangePasswordForm, \
    ChooseSiteForm
from bierapp.accounts.decorators import resolve_membership


@login_required
def password(request):
    form = ChangePasswordForm(instance=request.user, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        # Post message
        messages.success(request, "Password changed.")

        # Redirect back
        return redirect("bierapp.accounts.views.index")

    return render(request, "accounts_password.html", locals())


@login_required
def profile(request):
    form = ChangeProfileForm(
        instance=get_object_or_404(User, pk=request.user.id),
        data=request.POST or None, files=request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        # Post message
        messages.success(request, "Profile changed.")

        # Redirect back
        return redirect("bierapp.accounts.views.profile")
    return render(request, "accounts_profile.html", locals())


@login_required
def sites(request):
    memberships = request.user.memberships.all()

    return render(request, "accounts_sites.html", locals())


@login_required
@resolve_membership
def site(request, membership):
    """
    Show the site's information page.

    Note that `request.membership` can be different from `membership`. To
    prevent name clashes, `is_admin` is `True` if the current user is an admin
    of the requested site.
    """

    site = membership.site
    is_admin = membership.is_admin

    if request.membership.is_admin:
        memberships = site.memberships \
                          .order_by("is_hidden", "role") \
                          .prefetch_related("user")
    else:
        memberships = site.memberships\
                          .filter(is_hidden=False) \
                          .order_by("is_hidden", "role") \
                          .prefetch_related("user")

    membership_invites = site.membership_invites.all()

    return render(request, "accounts_site.html", locals())


@login_required
def site_create(request):
    form = SiteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        site = form.save()

        # Add current user as admin
        membership = UserMembership(
            site=site, user=request.user, role=ROLE_ADMIN).save()

        # Post message
        messages.success(request, "Site created.")

        # Redirect to site
        return redirect("bierapp.accounts.views.site", site_id=site.id)
    return render(request, "accounts_site_add.html", locals())


@login_required
@resolve_membership
def site_switch(request, membership):
    request.session["membership_id"] = membership.id

    return redirect(membership.site.get_absolute_url())


@login_required
@resolve_membership
def site_invite(request, membership):
    """
    Note that `request.membership` can be different from `membership`. To
    prevent name clashes, `is_admin` is `True` if the current user is an admin
    of the requested site.
    """

    site = membership.site
    is_admin = membership.is_admin

    if is_admin:
        roles = [
            (ROLE_GUEST, _("Guest")),
            (ROLE_MEMBER, _("Member"))]
    else:
        roles = [(ROLE_GUEST, _("Guest"))]

    form = UserMembershipInviteForm(
        membership.site, roles, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        # Update an existing invite instead of creating a new one. This will
        # create a new form, providing an instance. Since it is already valid,
        # the validation can be skipped this time.
        try:
            form = UserMembershipInviteForm(
                membership.site, roles, data=request.POST,
                instance=UserMembershipInvite.objects.get(
                    email=form.cleaned_data["email"], site=form.site))
        except UserMembershipInvite.DoesNotExist:
            pass

        invite = form.save()

        # Send email to new user. First check if the user has deleted his
        # account and doesn't want to receive any emails. If user does not
        # exists, he or she can be emailed.
        try:
            email_user = not User.objects.get(email=invite.email).is_deleted
        except User.DoesNotExist:
            email_user = True

        if email_user:
            pass  # TODO

        # Set success message
        messages.success(request, _(
            "User has been invited. He or she will receive an email to "
            "confirm membership. If the user does not have an account yet, "
            "he or she should register first."))

        return redirect(
            "bierapp.accounts.views.site", site_id=membership.site.id)
    return render(request, "accounts_site_invite.html", locals())


@login_required
def site_invite_done(request, site_id):
    return render(request, "accounts_site_invite_done.html", locals())


@login_required
def site_invite_revoke(request, site_id, invite_id):
    get_object_or_404(
        UserMembershipInvite, site__id=site_id, id=invite_id).delete()

    return redirect("bierapp.accounts.views.site", site_id=request.site.id)


@login_required
def invites(request):
    membership_invites = UserMembershipInvite.objects.filter(
        email=request.user.email)
    return render(request, "accounts_invites.html", locals())


@login_required
def invite_activate(request):
    accept = not request.GET.get("refuse")

    # Search invite. If it does not exist, the activate will result in an error
    # page.
    try:
        invite = UserMembershipInvite.objects.get(
            email=request.user.email, token=request.GET.get("token"))
    except UserMembershipInvite.DoesNotExist:
        invite = None

    # Convert it into real membership if accepted. Eventually delete the actual
    # invite.
    if invite:
        if accept:
            UserMembership(
                site=invite.site, user=request.user, role=invite.role).save()
        invite.delete()

    # Done
    return render(request, "accounts_invite_activate.html", locals())


def register(request):
    form = RegisterForm(data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        # Create user here
        form.save()

        # Log user in
        user = authenticate(
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password1"])
        auth_login(request, user)

        # Redirect to done
        return redirect("bierapp.accounts.views.register_done")

    return render(request, "accounts_register.html", locals())


def register_done(request):
    return render(request, "accounts_register_done.html", locals())


def login(request):
    """
    Login a user, the default action for pages that require login.

    In addition, this method supports the GET paramter `choose_site", which
    will redirect the user to a page for choosing a site. This is useful during
    OAUTH2 related requests.
    """

    is_authenticated = request.user.is_authenticated()
    is_choose_site = "choose_site" in request.GET or \
        "oauth2/authorize" in request.META.get("HTTP_REFERER", "")

    # Verify redirect URL
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, False)
    safe_url = is_safe_url(url=redirect_to, host=request.get_host())

    if not redirect_to or not safe_url:
        redirect_to = settings.LOGIN_REDIRECT_URL

    # Process post request
    form = AuthenticationForm(data=request.POST or None)

    if request.method == "POST":
        if "choose" in request.POST and is_authenticated:
            form = ChooseSiteForm(request.user.sites.all(), data=request.POST)

            if form.is_valid():
                site = form.cleaned_data["site"]
                membership = UserMembership.objects.get(
                    user=request.user, site=site)
                request.session["membership_id"] = membership.id

                return redirect(redirect_to)
            return render(request, "accounts_site_choose.html", locals())
        elif "login" in request.POST:
            if form.is_valid():
                auth_login(request, form.get_user())

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                if is_choose_site:
                    form = ChooseSiteForm(request.user.sites.all())
                    return render(
                        request, "accounts_site_choose.html", locals())
                return redirect(redirect_to)
    elif is_authenticated:
        if is_choose_site:
            form = ChooseSiteForm(request.user.sites.all())
            return render(request, "accounts_site_choose.html", locals())
        return redirect(redirect_to)
    else:
        request.session.set_test_cookie()

    # Default is to show login form
    return render(request, "accounts_login.html", locals())


def logout(request):
    # Logout
    auth_logout(request)

    # Done
    return redirect("bierapp.accounts.views.login")
