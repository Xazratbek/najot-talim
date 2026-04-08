from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError

class CustomUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ["username", "first_name","last_name","profile_picture","phone_number","address","email"]

    def clean_username(self):
        data = self.cleaned_data["username"]
        if data.startswith("j"):
            raise ValidationError("Ism j bilan boshlana olmaydi")

        return data

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        if data.endswith('bek'):
            raise ValidationError("Uka bizda ismi bek bilan tugediganlar ro'yxatdan o'tomedi oma")

        return data

    def clean_last_name(self):
        data = self.cleaned_data["last_name"]
        if data != data.lower():
            raise ValidationError("familiya hamma harflari kichkinada yozilsin")

        return data

    def clean_profile_picture(self):
        picture = self.cleaned_data["profile_picture"]
        if picture:
            pctr = picture.content_type
            if pctr not in ["JPEG","png","PNG"]:
                raise ValidationError("Shu file typelar qabul qilinadi: png")

        return picture

    def clean_address(self):
        address = self.cleaned_data["address"]
        if "Tashkent" not in address:
            raise ValidationError("Addressda Tashkent bo'lishi majbur")

        return address

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age < 18:
            raise ValidationError("Uka yoshiing kichkina ekan")

        return age


class CustomUserEditForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ["profile_picture","phone_number","username"]
