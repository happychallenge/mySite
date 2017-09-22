from PIL import Image
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
# from bootcamp.settings import ALLOWED_SIGNUP_DOMAINS

from .models import Profile

def SignupDomainValidator(value):
    # if '*' not in ALLOWED_SIGNUP_DOMAINS:
    #     try:
    #         domain = value[value.index("@"):]
    #         if domain not in ALLOWED_SIGNUP_DOMAINS:
    #             raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501

    #     except Exception:
    #         raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501
    pass

def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')

def validate_password_strength(value):
    """Validates that a password is as least 7 characters long and has at least
    1 digit and 1 letter.
    """
    min_length = 8

    if len(value) < min_length:
        raise ValidationError(_('Password must be at least {0} characters '
                                'long.').format(min_length))
    # check for digit
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must contain at least 1 digit.'))

    # check for letter
    if not any(char.isalpha() for char in value):
        raise ValidationError(_('Password must contain at least 1 letter.'))

class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.HiddenInput())  # noqa: E261
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
        max_length=75)
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        label="Name",
        max_length=75)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm your password",
        required=True)

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'first_name', 'password', 'confirm_password', ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators.append(UniqueEmailValidator)
        self.fields['email'].validators.append(SignupDomainValidator)
        self.fields['password'].validators.append(validate_password_strength)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Passwords don\'t match'])
        return self.cleaned_data


# records/forms.py
#
# class ArticleForm(forms.ModelForm):
#   title = forms.CharField(
#       widgets = forms.TextInput(attrs={'class':'form-control'}), max_length=255)
#   title = forms.CharField(
#       widgets = forms.HiddenInput()
#   title = forms.CharField(
#       widgets = forms.Textarea(attrs={'class':'form-control'}), max_length=4000)
#   title = forms.CharField(
#       widgets = forms.TextInput(attrs={'class':'form-control'}), max_length=4000, required=False, help_text='.....')
#
#


class ProfileForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    # existed = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ['picture', 'x', 'y', 'width', 'height', ]
        widgets = {
            'picture': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self):
        profile = super(ProfileForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')
        image = Image.open(profile.picture)
        cropped_image = image.crop((x, y, width+x, height+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(profile.picture.path)

        return profile