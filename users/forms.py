from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Address

User = get_user_model()

WIDGET = lambda placeholder, cls='form-control': forms.TextInput(attrs={'class': cls, 'placeholder': placeholder})
EMAIL_WIDGET = lambda placeholder: forms.EmailInput(attrs={'class': 'form-control', 'placeholder': placeholder})
PASSWORD_WIDGET = lambda placeholder: forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': placeholder})


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=PASSWORD_WIDGET('Create a strong password'))
    password2 = forms.CharField(label='Confirm Password', widget=PASSWORD_WIDGET('Repeat your password'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': WIDGET('First name'),
            'last_name': WIDGET('Last name'),
            'email': EMAIL_WIDGET('your@email.com'),
            'username': WIDGET('Choose a username'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        if p1 and len(p1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email'].lower()
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=EMAIL_WIDGET('your@email.com'), label='Email')
    password = forms.CharField(widget=PASSWORD_WIDGET('Your password'), label='Password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar', 'bio', 'date_of_birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 555 0000'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us a little about yourself…'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'style': 'display:none;'}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'full_name', 'phone', 'address_line_1', 'address_line_2',
                  'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 555 0000'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street address'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apt, suite, unit (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State / Province'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
