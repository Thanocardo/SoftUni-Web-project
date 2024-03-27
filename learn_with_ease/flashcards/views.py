from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views


from learn_with_ease.flashcards.forms import LearnWithEasyFlashCardCreation, LearnWithEasyFolderCreation
from learn_with_ease.flashcards.models import FlashCards, Folders
from learn_with_ease.user_profile.views import OwnerRequiredMixin


# Create your views here.

class LibraryView(LoginRequiredMixin, views.TemplateView):

    login_url = reverse_lazy('login')
    template_name = 'flashcards/library.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.request.user.id
        context['flashcards'] = FlashCards.objects.filter(profile_id=profile_id, archived=False)
        context['folders'] = Folders.objects.filter(profile_id=profile_id, archived=False)
        return context


class ArchiveView(LoginRequiredMixin, views.TemplateView):

    login_url = reverse_lazy('login')
    template_name = 'flashcards/archive.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.request.user.id
        context['flashcards'] = FlashCards.objects.filter(profile_id=profile_id, archived=True)
        context['folders'] = Folders.objects.filter(profile_id=profile_id, archived=True)
        return context


class FlashCardsCreationView(LoginRequiredMixin, views.CreateView):

    login_url = reverse_lazy('login')
    form_class = LearnWithEasyFlashCardCreation
    success_url = reverse_lazy("library")
    template_name = 'flashcards/flashcard_creation.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_profile'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        form.instance.profile_id = self.request.user.id
        return super().form_valid(form)


class FlashCardsUpdateView(LoginRequiredMixin, views.UpdateView):

    login_url = reverse_lazy('login')
    form_class = LearnWithEasyFlashCardCreation
    success_url = reverse_lazy("library")
    template_name = "flashcards/flashcard_edit.html"

    def get_queryset(self):
        return FlashCards.objects.filter(profile_id=self.request.user.id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_profile'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        obj = form.instance

        if obj.archived:
            if obj.folder:
                if obj.folder.archived:
                    return super().form_valid(form)
                obj.folder = None
        else:
            if obj.folder:
                if obj.folder.archived:
                    obj.folder = None

        return super().form_valid(form)


class FlashCardsDeleteView(LoginRequiredMixin, views.DeleteView):
    # TODO:make it so it deletes images from folder
    login_url = reverse_lazy('login')
    template_name = 'flashcards/flashcard_delete.html'
    success_url = reverse_lazy("library")

    def get_queryset(self):
        return FlashCards.objects.filter(profile_id=self.request.user.id)


class FolderView(LoginRequiredMixin, views.DetailView):

    login_url = reverse_lazy('login')
    model = Folders
    template_name = 'flashcards/folder.html'
    context_object_name = 'folder'

    def dispatch(self, request, *args, **kwargs):
        folder = self.get_object()
        if folder.profile_id and folder.profile_id != request.user.id:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        folder = self.get_object()
        context['flashcards'] = folder.flashcards.all()
        return context


class FolderCreationView(LoginRequiredMixin, views.CreateView):

    login_url = reverse_lazy('login')
    form_class = LearnWithEasyFolderCreation
    success_url = reverse_lazy("library")
    template_name = 'flashcards/folder_creation.html'

    def form_valid(self, form):
        form.instance.profile_id = self.request.user.id
        return super().form_valid(form)


class FolderEditView(LoginRequiredMixin, views.UpdateView):

    login_url = reverse_lazy('login')
    form_class = LearnWithEasyFolderCreation
    success_url = reverse_lazy("library")
    template_name = "flashcards/folder_edit.html"

    def get_queryset(self):
        return Folders.objects.filter(profile_id=self.request.user.id)

    def form_valid(self, form):
        folder = form.instance

        if folder.archived:
            folder.flashcards.update(archived=True)
        else:
            folder.flashcards.update(archived=False)
            
        return super().form_valid(form)


class FolderDeleteView(LoginRequiredMixin, views.DeleteView):
    # TODO:make it so it deletes images from folder
    login_url = reverse_lazy('login')
    template_name = 'flashcards/folder_delete.html'
    success_url = reverse_lazy("library")

    def get_queryset(self):
        return Folders.objects.filter(profile_id=self.request.user.id)
