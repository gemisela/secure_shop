from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Prénom",
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Votre prénom",
            "autocomplete": "given-name"
        })
    )
    last_name = forms.CharField(
        label="Nom",
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Votre nom",
            "autocomplete": "family-name"
        })
    )
    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={
            "placeholder": "exemple@email.com",
            "autocomplete": "email"
        })
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Un compte existe déjà avec cette adresse e-mail.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        user.email = self.cleaned_data["email"].strip().lower()
        user.username = user.email
        if commit:
            user.save()
        return user
