from django import forms
from .models import CustomUser
from django.forms import ValidationError

class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'parolni kiriting'})
    )
    password2 = forms.CharField(
        label='parolni tasdiqlash',
        widget=forms.PasswordInput(attrs={'placeholder': 'parolni qayta kiriting'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number' , 'username', 'password' ,'photo']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 8:
            raise ValidationError("parol kamida 8ta belgidan iborat bo'lishi kerak")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError("parollar mos emas")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parol'}),
        label="Yangi parol"
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username', 'photo']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ism'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Familiya'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+998 ...'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }
