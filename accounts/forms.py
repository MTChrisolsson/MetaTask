# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Organization

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    organization = forms.CharField(
        max_length=70,
        required=False,
        help_text="Enter organization name to create a new one (optional)"
    )

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'organization', 'password1', 'password2')
        exclude = ('organization',)

    def clean_organization(self):
        """
        Validate that the organization name doesn't already exist if provided
        """
        organization_name = self.cleaned_data.get('organization')
        
        if organization_name:
            # Check if organization with this name already exists
            if Organization.objects.filter(name__iexact=organization_name).exists():
                raise forms.ValidationError(
                    f"An organization with the name '{organization_name}' already exists. "
                    "Please choose a different name or contact the organization administrator."
                )
        
        return organization_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        organization_name = self.cleaned_data.get('organization')
        if organization_name:
            # Create new organization
            from django.utils.text import slugify
            organization, created = Organization.objects.get_or_create(
                name=organization_name,
                defaults={'slug': slugify(organization_name), 'is_active': True}
            )
            print(f"Organization object: {organization}" )
            print(f"Type of organization: {type(organization)}")
            user.organization = organization

        if commit:
            user.save()
        return user

class AddMemberForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned