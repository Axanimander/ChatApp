from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_slug
from django.contrib.auth.models import User
from . import models
def must_be_unique(value):
    user = User.objects.filter(email=value)
    if len(user) > 0:
        raise forms.ValidationError("Email Already in Use")
    return value

class roomForm(forms.Form):
    room = forms.CharField(
        label='RoomTitle',
        required=True,
        max_length=50
    )

    def save(self, request):
        room_instance = models.roomModel()
        room_instance.roomName=self.cleaned_data["room"]
        room_instance.creator=request.user
        room_instance.save()
        return room_instance
class messageForm(forms.Form):
    message = forms.CharField(
        label="Content",
        required=True,
        max_length = 240,
    )
    def save(self,request,room_id):
        room_instance = models.roomModel.objects.get(id=room_id)
        message_instance = models.message()
        message_instance.room = room_instance
        message_instance.content = self.cleaned_data["message"]
        message_instance.author = request.user
        message_instance.save()
        return message_instance

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )

    class Meta:
        model = User
        fields = ("username", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user