from django import forms

from learn_with_ease.flashcards.models import FlashCards, Folders


class LearnWithEasyFlashCardCreation(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if user_profile:
            if self.instance.archived:
                self.fields['folder'].queryset = Folders.objects.filter(profile_id=user_profile, archived=True)
            else:
                self.fields['folder'].queryset = Folders.objects.filter(profile_id=user_profile)

    class Meta:
        model = FlashCards
        fields = ('question', 'question_picture', 'answer', 'answer_picture', 'shuffle_question_and_answer', 'only_show_answer', 'folder', 'archived')


class LearnWithEasyFolderCreation(forms.ModelForm):

    class Meta:
        model = Folders
        fields = ('folder_photo', 'folder_name', 'archived')

