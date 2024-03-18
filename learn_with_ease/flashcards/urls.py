from django.urls import path, include

from learn_with_ease.flashcards.views import FlashCardsCreationView, LibraryView, FlashCardsUpdateView, \
    FlashCardsDeleteView, FolderView, ArchiveView, FolderEditView, FolderCreationView, FolderDeleteView

urlpatterns = (
    path('', LibraryView.as_view(), name='library'),
    path('archive', ArchiveView.as_view(), name='flashcards_archive'),
    path('creation/', include([
        path('/flashcard/', FlashCardsCreationView.as_view(), name='flashcard_creation'),
        path('/folder/', FolderCreationView.as_view(), name='folder_creation'),
    ])),
    path('flashcards/<int:pk>/<slug:slug>/', include([
        path('edit/', FlashCardsUpdateView.as_view(), name='flashcard_edit'),
        path('delete/', FlashCardsDeleteView.as_view(), name='flashcard_delete'),
    ])),
    path('folder/<int:pk>/<slug:slug>/', include([
        path('', FolderView.as_view(), name='flashcards_folder'),
        path('edit/', FolderEditView.as_view(), name='folder_edit'),
        path('delete/', FolderDeleteView.as_view(), name='folder_delete'),
    ])),
)