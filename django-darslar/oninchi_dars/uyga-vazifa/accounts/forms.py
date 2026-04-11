from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError

class CustomUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ["username", "first_name","last_name","avatar","phone_number","email"]

class CustomUserEditForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ["avatar","phone_number","username"]
