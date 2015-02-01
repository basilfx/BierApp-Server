from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse
from django.conf import settings

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

from bierapp.accounts.models import User, UserMembershipInvite, UserMembership, Site
from bierapp.accounts.forms import RegisterForm, UserMembershipInviteForm, SiteForm, ChangeProfileForm, AuthenticationForm, ChangePasswordForm, ChooseSiteForm
from bierapp.accounts.decorators import resolve_membership, resolve_site, site_admin_required

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
    form = ChangeProfileForm(instance=request.user, data=request.POST or None, files=request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        # Post message
        messages.success(request, "Profile changed.")

        # Redirect back
        return redirect("bierapp.accounts.views.profile")
    return render(request, "accounts_profile.html", locals())

@login_required
def sites(request):
    sites = request.user.sites.all()

    return render(request, "accounts_sites.html", locals())

@login_required
@resolve_membership
def site(request, membership):
    site = membership.site

    if request.membership.is_admin:
        memberships = site.memberships.all().order_by("is_hidden")
    else:
        memberships = site.memberships.filter(is_hidden=False).order_by("is_hidden")

    membership_invites = site.membership_invites.all()

    return render(request, "accounts_site.html", locals())

@login_required
def site_create(request):
    form = SiteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        site = form.save()

        # Add current user as admin
        membership = UserMembership(site=site, user=request.user, is_admin=True).save()

        # Post message
        messages.success(request, "Site created.")

        # Redirect to site
        return redirect("bierapp.accounts.views.site", id=site.id)
    return render(request, "accounts_site_add.html", locals())

@login_required
@resolve_membership
def site_switch(request, membership):
    request.session["membership_id"] = membership.id

    return redirect(membership.site.get_absolute_url())

@login_required
@resolve_membership
@site_admin_required
def site_invite(request, membership):
    form = UserMembershipInviteForm(membership.site, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        invite = form.save()

    return render(request, "accounts_site_invite.html", locals())

@login_required
@resolve_site
def site_invite_activate(request, site):
    # Search invite
    try:
        invite = UserMembershipInvite.objects.get(site=site, email=request.GET["email"], token=request.GET["token"])
    except UserMembershipInvite.DoesNotExist:
        return render(request, "accounts_site_invite_activate.html", locals())

    # Search user for given email
    try:
        user = User.objects.get(email=invite.email)
    except User.DoesNotExist:
        return redirect("bierapp.accounts.views.register")

    # Convert it into real membership and delete invite
    UserMembership(site=site, user=user).save()
    invite.delete()

    # Done
    return render(request, "accounts_site_invite_activate.html", locals())

def register(request):
    form = RegisterForm(data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        # Create user here
        form.save()

        # Log user in
        user = authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password1"])
        auth_login(request, user)

        # Redirect to done
        return redirect("bierapp.accounts.views.register_done")

    return render(request, "accounts_register.html", locals())

def register_done(request):
    return render(request, "accounts_register_done.html", locals())

def login(request):
    """
    Login a user, the default action for pages that require login.

    In addition, this method supports the GET paramter `choose_site", which will
    redirect the user to a page for choosing a site. This is useful during
    OAUTH2 related requests.
    """

    is_authenticated = request.user.is_authenticated()
    is_choose_site = "choose_site" in request.GET or "oauth2/authorize" in request.META.get("HTTP_REFERER", "")

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
                membership = UserMembership.objects.get(user=request.user, site=site)
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
                    return render(request, "accounts_site_choose.html", locals())
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