from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from learn_with_ease.flashcards.models import FlashCards, Folders
from learn_with_ease.posts.forms import LearnWithEasyPostEdit, LearnWithEasyPostCreation, LearnWithEasyCommentCreation
from learn_with_ease.posts.models import Posts, Comments


# Create your views here.
class PostsView(views.TemplateView):

    template_name = 'posts/browse_posts.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Posts.objects.all().order_by('-likes', 'post_name')
        return context


class PostCreationView(LoginRequiredMixin, views.CreateView):

    login_url = reverse_lazy('login')
    form_class = LearnWithEasyPostCreation
    success_url = reverse_lazy("browse_posts")
    template_name = 'posts/post_creation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(user_profile=self.request.user.profile)
        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.profile = self.request.user.profile
        self.object.save()

        selected_cards = form.cleaned_data['select_cards']
        selected_folders = form.cleaned_data['select_folders']

        for card in selected_cards:
            new_card = card.copy()
            new_card.post = self.object
            new_card.save()

        for folder in selected_folders:
            new_folder = folder.copy()
            new_folder.post = self.object
            new_folder.save()

        return super().form_valid(form)


class PostAndCommentsDetailsView(LoginRequiredMixin, views.CreateView):

    login_url = reverse_lazy('login')
    template_name = 'posts/post_details.html'
    form_class = LearnWithEasyCommentCreation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_data'] = Posts.objects.filter(id=self.request.resolver_match.kwargs['pk']).first()
        context['cards'] = FlashCards.objects.filter(post_id=self.request.resolver_match.kwargs['pk'])
        context['folders'] = Folders.objects.filter(post_id=self.request.resolver_match.kwargs['pk'])
        context['comments'] = Comments.objects.filter(post_id=self.request.resolver_match.kwargs['pk']).order_by('-likes')
        return context

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.instance.post = Posts.objects.filter(id=self.request.resolver_match.kwargs['pk']).first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_details', kwargs={'pk': self.request.resolver_match.kwargs['pk'], 'slug': self.request.resolver_match.kwargs['slug']})


class PostDataDownloadView(LoginRequiredMixin, views.TemplateView):

    login_url = reverse_lazy('login')
    template_name = 'posts/post_download.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = FlashCards.objects.filter(post_id=context['pk'])
        context['folders'] = Folders.objects.filter(post_id=context['pk'])
        return context

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Posts, id=pk)

        cards = post.flashcards.all()
        folders = post.folders.all()

        requesting_profile = request.user.profile

        for card in cards:
            new_card = card.copy()
            new_card.profile = requesting_profile
            new_card.save()

        for folder in folders:
            new_folder = folder.copy()
            new_folder.profile = requesting_profile
            new_folder.save()

        return redirect('library')


class PostEditView(LoginRequiredMixin, views.UpdateView):

    model = Posts
    login_url = reverse_lazy('login')
    form_class = LearnWithEasyPostEdit
    template_name = "posts/post_edit.html"

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.profile.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('post_details', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


class PostDeleteView(LoginRequiredMixin, views.DeleteView):
    # TODO:make it so it deletes images from folder
    login_url = reverse_lazy('login')
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy("browse_posts")

    def get_queryset(self):
        return Posts.objects.filter(profile_id=self.request.user.id)


class CommentEditView(LoginRequiredMixin, views.UpdateView):

    model = Comments
    login_url = reverse_lazy('login')
    form_class = LearnWithEasyCommentCreation
    template_name = "posts/comment_edit.html"

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.profile.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        com_pk = self.kwargs.get('com_pk')
        return get_object_or_404(queryset, pk=com_pk)

    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post_details', kwargs={'pk': comment.post.id, 'slug': comment.post.slug})


class CommentDeleteView(LoginRequiredMixin, views.DeleteView):

    login_url = reverse_lazy('login')
    template_name = 'posts/comment_delete.html'

    def get_queryset(self):
        return Comments.objects.filter(profile_id=self.request.user.id)

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        com_pk = self.kwargs.get('com_pk')
        return get_object_or_404(queryset, pk=com_pk)

    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post_details', kwargs={'pk': comment.post.id, 'slug': comment.post.slug})
