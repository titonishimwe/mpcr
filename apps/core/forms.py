from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your Full Name *",
                    "required": "required",
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your Email Address *",
                    "required": "required",
                    "autocomplete": "email",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your Phone Number (optional)",
                    "autocomplete": "tel",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Subject of your message *",
                    "required": "required",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 5,
                    "placeholder": "Write your inquiry, partnership proposal, or feedback here... *",
                    "required": "required",
                }
            ),
        }
