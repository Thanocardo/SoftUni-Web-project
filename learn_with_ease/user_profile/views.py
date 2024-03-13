from django.contrib.auth import views as auth_view, login, logout
from django.contrib.auth import mixins as auth_mixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from learn_with_ease.user_profile.forms import LearnWithEasyUserCreationCreationForm
from learn_with_ease.user_profile.models import ProfileData


# Create your views here.

class OwnerRequiredMixin:
    user_field = "user"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj_user = getattr(obj, self.user_field, None)
        if not self.request.user.is_authenticated or obj_user != self.request.user:
            raise PermissionDenied

        return obj


class LoginUserView(auth_view.LoginView):
    template_name = 'user_profile/login.html'
    success_url = reverse_lazy('main_page')
    redirect_authenticated_user = True


class SignUpUserView(views.CreateView):
    form_class = LearnWithEasyUserCreationCreationForm
    template_name = "user_profile/signup_user.html"
    success_url = reverse_lazy("main_page")
    redirect_authenticated_user = True

    def form_valid(self, form):

        result = super().form_valid(form)

        login(self.request, form.user)

        return result


class ProfileView(views.DetailView):
    queryset = ProfileData.objects.prefetch_related('user').all()
    template_name = 'user_profile/profile.html'
    context_object_name = 'profile'


class ProfileUpdateView(OwnerRequiredMixin, views.UpdateView):
    # TODO: maybe make it profile/edit
    queryset = ProfileData.objects.all()
    template_name = "user_profile/profile_edit.html"
    fields = ("username", "profile_description", "age", "profile_picture", "gender")

    def get_success_url(self):
        return reverse("profile", kwargs={
            "slug": self.object.slug,
        })

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form


def sign_out_user(request):
    logout(request)
    return redirect('main_page')


class ProfileDeleteView(OwnerRequiredMixin, views.DeleteView):
    queryset = ProfileData.objects.all()
    template_name = "user_profile/profile_delete.html"

    def form_valid(self, request, *args, **kwargs):

        user_profile = self.get_object()

        user_profile.user.is_active = False
        user_profile.user.save()

        logout(self.request)

        return HttpResponseRedirect(reverse_lazy('main_page'))

