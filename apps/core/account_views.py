from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from smtplib import SMTPException
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.http import require_POST

from .account_forms import (
    AccountPasswordChangeForm,
    DeactivateAccountForm,
    EmailChangeForm,
    ProfileForm,
    SessionLogoutForm,
    StaffPasswordResetForm,
)
from .dashboard_views import _staff_required, dashboard_context
from .models import AccountActivity, StaffProfile

EMAIL_TOKEN_MAX_AGE = 60 * 60 * 24
email_signer = TimestampSigner(salt="mpcr-email-confirm")


def log_activity(user, action):
    AccountActivity.objects.create(user=user, action=action)


def get_profile(user):
    profile, _created = StaffProfile.objects.get_or_create(user=user)
    return profile


def _sessions_for_user(user):
    user_id = str(user.pk)
    for session in Session.objects.filter(expire_date__gte=timezone.now()):
        data = session.get_decoded()
        if str(data.get("_auth_user_id")) == user_id:
            yield session


def logout_other_sessions(request):
    current = request.session.session_key
    for session in _sessions_for_user(request.user):
        if session.session_key != current:
            session.delete()


def logout_all_sessions(user):
    for session in _sessions_for_user(user):
        session.delete()


def active_staff_exists_besides(user):
    from django.contrib.auth import get_user_model

    return get_user_model().objects.filter(is_staff=True, is_active=True).exclude(pk=user.pk).exists()


@_staff_required
def account_view(request):
    profile = get_profile(request.user)
    return render(
        request,
        "dashboard/account.html",
        dashboard_context(
            request,
            page_title="Account - Dashboard",
            resource="account",
            profile=profile,
            activities=request.user.account_activities.all()[:8],
        ),
    )


@_staff_required
def account_edit(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        log_activity(request.user, "Profile details updated")
        messages.success(request, "Account details updated.")
        return redirect("account")

    return render(
        request,
        "dashboard/account_form.html",
        dashboard_context(
            request,
            page_title="Edit account - Dashboard",
            resource="account",
            form=form,
            heading="Edit account",
            intro="You can change your name and username. Email is changed separately so it can be verified first.",
        ),
    )


@_staff_required
def account_email(request):
    profile = get_profile(request.user)
    form = EmailChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        pending = form.cleaned_data["email"]
        profile.pending_email = pending
        profile.save(update_fields=["pending_email", "updated_at"])
        token = email_signer.sign(f"{request.user.pk}:{pending}")
        confirm_url = request.build_absolute_uri(reverse("account_email_confirm", kwargs={"token": token}))
        try:
            send_mail(
                subject="Confirm your MPCR email address",
                message=(
                    "Confirm this new email address for your MPCR account.\n\n"
                    f"{confirm_url}\n\n"
                    "This link expires in 24 hours. Until you confirm it, password recovery "
                    "will continue to use your current email address.\n"
                ),
                from_email=None,
                recipient_list=[pending],
                fail_silently=False,
            )
        except (SMTPException, OSError):
            messages.error(request, "The confirmation email could not be sent. Try again later.")
            return redirect("account_email")
        log_activity(request.user, "Email change requested")
        messages.success(
            request,
            "A confirmation link was sent to the new address. Your current email stays active until you confirm it.",
        )
        return redirect("account")

    return render(
        request,
        "dashboard/account_form.html",
        dashboard_context(
            request,
            page_title="Change email - Dashboard",
            resource="account",
            form=form,
            heading="Change email",
            intro="Enter your current password. The new address is not used for password recovery until you confirm it.",
            pending_email=profile.pending_email,
        ),
    )


@login_required(login_url="dashboard_login")
def account_email_confirm(request, token):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to confirm this email.")
        return redirect("dashboard_login")

    try:
        payload = email_signer.unsign(token, max_age=EMAIL_TOKEN_MAX_AGE)
        user_id, pending = payload.split(":", 1)
    except (BadSignature, SignatureExpired, ValueError):
        messages.error(request, "This email confirmation link is invalid or has expired.")
        return redirect("account")

    profile = get_profile(request.user)
    if str(request.user.pk) != user_id or profile.pending_email.lower() != pending.lower():
        messages.error(request, "This email confirmation link is invalid or has already been used.")
        return redirect("account")

    request.user.email = pending
    request.user.save(update_fields=["email"])
    profile.pending_email = ""
    profile.save(update_fields=["pending_email", "updated_at"])
    log_activity(request.user, "Email address confirmed")
    messages.success(request, "Email address confirmed. Password recovery now uses this address.")
    return redirect("account")


@_staff_required
def account_password(request):
    form = AccountPasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        update_session_auth_hash(request, request.user)
        logout_other_sessions(request)
        log_activity(request.user, "Password changed")
        messages.success(request, "Password changed. Other signed-in sessions have been signed out.")
        return redirect("account")

    return render(
        request,
        "dashboard/account_form.html",
        dashboard_context(
            request,
            page_title="Change password - Dashboard",
            resource="account",
            form=form,
            heading="Change password",
            intro="If you believe someone knows your password, change it now. Other sessions will be signed out.",
        ),
    )


@_staff_required
@require_POST
def account_logout_others(request):
    form = SessionLogoutForm(request.user, request.POST)
    if form.is_valid():
        logout_other_sessions(request)
        log_activity(request.user, "Signed out other sessions")
        messages.success(request, "Other sessions have been signed out. This browser stays signed in.")
    else:
        messages.error(request, "Current password is incorrect.")
    return redirect("account")


@_staff_required
def account_deactivate(request):
    if not active_staff_exists_besides(request.user):
        messages.error(request, "The last active admin account cannot be deactivated.")
        return redirect("account")

    form = DeactivateAccountForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        request.user.is_active = False
        request.user.save(update_fields=["is_active"])
        log_activity(request.user, "Account deactivated")
        logout_all_sessions(request.user)
        logout(request)
        messages.success(request, "Your account has been deactivated.")
        return redirect("dashboard_login")

    return render(
        request,
        "dashboard/account_form.html",
        dashboard_context(
            request,
            page_title="Deactivate account - Dashboard",
            resource="account",
            form=form,
            heading="Deactivate account",
            intro="This signs you out everywhere and stops sign-in. Your records are kept. An administrator can reactivate the account later.",
            submit_label="Deactivate account",
        ),
    )


def console_email_enabled():
    return settings.EMAIL_BACKEND.endswith("console.EmailBackend")


class DashboardPasswordResetView(PasswordResetView):
    template_name = "dashboard/password_reset_form.html"
    email_template_name = "dashboard/password_reset_email.txt"
    subject_template_name = "dashboard/password_reset_subject.txt"
    form_class = StaffPasswordResetForm
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        if console_email_enabled():
            links = []
            for user in form.get_users(form.cleaned_data["email"]):
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                links.append(
                    self.request.build_absolute_uri(
                        reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
                    )
                )
            self.request.session["dev_reset_links"] = links
        return super().form_valid(form)


class DashboardPasswordResetDoneView(PasswordResetDoneView):
    template_name = "dashboard/password_reset_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["console_email"] = console_email_enabled()
        context["dev_reset_links"] = self.request.session.pop("dev_reset_links", [])
        return context


class DashboardPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "dashboard/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs["class"] = "form-input"
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.user
        logout_all_sessions(user)
        log_activity(user, "Password reset completed")
        return response


class DashboardPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "dashboard/password_reset_complete.html"
