from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import PasswordResetForm

User = get_user_model()


def style_fields(form):
    for field in form.fields.values():
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.setdefault("class", "dash-check")
        else:
            field.widget.attrs.setdefault("class", "form-input")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_fields(self)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.exclude(pk=self.instance.pk).filter(username__iexact=username).exists():
            raise forms.ValidationError("That username is already in use.")
        return username


class EmailChangeForm(forms.Form):
    email = forms.EmailField(label="New email")
    current_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        style_fields(self)

    def clean_current_password(self):
        password = self.cleaned_data["current_password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("Current password is incorrect.")
        return password

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if email == (self.user.email or "").lower():
            raise forms.ValidationError("That is already your email address.")
        if User.objects.exclude(pk=self.user.pk).filter(email__iexact=email).exists():
            raise forms.ValidationError("That email is already in use.")
        return email


class AccountPasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    new_password = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=" ".join(password_validation.password_validators_help_texts()),
    )
    confirm_password = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        style_fields(self)

    def clean_current_password(self):
        password = self.cleaned_data["current_password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("Current password is incorrect.")
        return password

    def clean_new_password(self):
        password = self.cleaned_data["new_password"]
        password_validation.validate_password(password, self.user)
        if self.user.check_password(password):
            raise forms.ValidationError("Choose a password you have not used before.")
        return password

    def clean(self):
        cleaned = super().clean()
        new_password = cleaned.get("new_password")
        confirm = cleaned.get("confirm_password")
        if new_password and confirm and new_password != confirm:
            self.add_error("confirm_password", "The two passwords do not match.")
        return cleaned

    def save(self):
        self.user.set_password(self.cleaned_data["new_password"])
        self.user.save(update_fields=["password"])
        return self.user


class SessionLogoutForm(forms.Form):
    current_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        style_fields(self)

    def clean_current_password(self):
        password = self.cleaned_data["current_password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("Current password is incorrect.")
        return password


class DeactivateAccountForm(forms.Form):
    current_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    confirm = forms.BooleanField(
        label="I understand this will deactivate my account and sign me out.",
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        style_fields(self)

    def clean_current_password(self):
        password = self.cleaned_data["current_password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("Current password is incorrect.")
        return password


class StaffPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        return (user for user in super().get_users(email) if user.is_staff)
