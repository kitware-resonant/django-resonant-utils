from django import forms
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


# Django-Allauth further inherits from this form, and adds the typical "username", "email", etc.
# fields.
class FullNameSignupForm(forms.Form):
    """
    A Django-Allauth signup form which prompts for a user's first and last name.

    To use this, set the setting:
    ACCOUNT_SIGNUP_FORM_CLASS = 'resonant_utils.allauth.FullNameSignupForm'
    """

    first_name = forms.CharField(
        max_length=150,
        label=_("First name"),
        widget=forms.TextInput(
            attrs={"placeholder": _("First name"), "autocomplete": "given-name"}
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        label=_("Last name"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Last name"), "auto complete": "family-name"}
        ),
    )

    field_order = [
        # Any undefined fields in this list are just ignored
        "first_name",
        "last_name",
        "email",
        "email2",
        "username",
        "password1",
        "password2",
    ]

    def signup(self, request: HttpRequest, user: AbstractUser) -> None:
        # Allauth requires this method to be defined
        pass
