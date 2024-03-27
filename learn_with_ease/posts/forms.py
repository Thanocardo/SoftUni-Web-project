from django import forms

from learn_with_ease.flashcards.models import FlashCards, Folders
from learn_with_ease.posts.models import Posts, Comments


class LearnWithEasyPostEdit(forms.ModelForm):

    selected_cards = forms.ModelMultipleChoiceField(queryset=FlashCards.objects.all(), widget=forms.CheckboxSelectMultiple, required=False,)
    selected_folders = forms.ModelMultipleChoiceField(queryset=Folders.objects.all(), widget=forms.CheckboxSelectMultiple, required=False,)
    select_cards = forms.ModelMultipleChoiceField(queryset=FlashCards.objects.all(), widget=forms.CheckboxSelectMultiple, required=False,)
    select_folders = forms.ModelMultipleChoiceField(queryset=Folders.objects.all(), widget=forms.CheckboxSelectMultiple, required=False,)

    class Meta:
        model = Posts
        fields = ['post_name', 'description', 'post_photo', 'selected_cards', 'selected_folders', 'select_cards', 'select_folders']

    def __init__(self, *args, **kwargs):
        post_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if post_instance:
            self.fields['select_cards'].queryset = post_instance.profile.flashcards.all().filter(archived=False, folder_id=None)
            self.fields['select_folders'].queryset = post_instance.profile.folders.all().filter(archived=False)
            self.fields['selected_cards'].initial = FlashCards.objects.filter(post_id=post_instance.id)
            self.fields['selected_folders'].initial = Folders.objects.filter(post_id=post_instance.id)
            self.fields['selected_cards'].queryset = FlashCards.objects.filter(post_id=post_instance.id)
            self.fields['selected_folders'].queryset = Folders.objects.filter(post_id=post_instance.id)

    def save(self, commit=True):
        post = super().save(commit=False)

        initial_cards = list(FlashCards.objects.filter(post_id=post.id))
        initial_folders = list(Folders.objects.filter(post_id=post.id))

        if commit:
            post.save()

            cleaned_cards = self.cleaned_data.get('selected_cards', [])
            cleaned_folders = self.cleaned_data.get('selected_folders', [])
            new_cards = self.cleaned_data.get('select_cards', [])
            new_folders = self.cleaned_data.get('select_folders', [])

            for card in initial_cards:
                if card not in cleaned_cards:
                    card.delete()

            for folder in initial_folders:
                if folder not in cleaned_folders:
                    folder.delete()

            for card in new_cards:
                new_card = card.copy()
                new_card.profile = None
                new_card.post = post
                new_card.save()

            for folder in new_folders:
                new_folder = folder.copy()
                new_folder.profile = None
                new_folder.post = post
                new_folder.save()

        return post


class LearnWithEasyPostCreation(forms.ModelForm):

    select_cards = forms.ModelMultipleChoiceField(queryset=FlashCards.objects.all(), widget=forms.CheckboxSelectMultiple, required=False,)
    select_folders = forms.ModelMultipleChoiceField(queryset=Folders.objects.all(), widget=forms.CheckboxSelectMultiple, required=False,)

    class Meta:
        model = Posts
        fields = ['post_name', 'description', 'select_cards', 'select_folders', 'post_photo']

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if user_profile:
            self.fields['select_cards'].queryset = FlashCards.objects.filter(profile=user_profile, archived=False, folder_id=None).order_by('question')
            self.fields['select_folders'].queryset = Folders.objects.filter(profile=user_profile, archived=False).order_by('folder_name')


class LearnWithEasyCommentCreation(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }