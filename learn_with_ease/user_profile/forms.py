from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from learn_with_ease.user_profile.models import ProfileData

UserModel = get_user_model()


class LearnWithEasyUserCreationCreationForm(auth_forms.UserCreationForm):
    user = None
    Username = forms.CharField()

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('Username', 'email',)

    def save(self, commit=True):
        self.user = super().save(commit=commit)

        profile = ProfileData(
            username=self.cleaned_data["Username"],
            user=self.user,

        )

        if commit:
            profile.save()

        return self.user
