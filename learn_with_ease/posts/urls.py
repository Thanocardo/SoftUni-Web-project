from django.urls import path, include

from learn_with_ease.posts.views import PostsView, PostCreationView, PostEditView, PostDeleteView, \
    PostDataDownloadView, PostAndCommentsDetailsView, CommentEditView, CommentDeleteView

urlpatterns = (
    path('', PostsView.as_view(), name='browse_posts'),
    path('creation', PostCreationView.as_view(), name='post_creation'),
    path('<int:pk>/<slug:slug>/', include([
        path('details', PostAndCommentsDetailsView.as_view(), name='post_details'),
        path('edit', PostEditView.as_view(), name='post_edit'),
        path('delete', PostDeleteView.as_view(), name='post_delete'),
        path('download', PostDataDownloadView.as_view(), name='post_download'),
        path('<int:com_pk>/comment/edit', CommentEditView.as_view(), name='comment_edit'),
        path('<int:com_pk>/comment/delete', CommentDeleteView.as_view(), name='comment_delete'),

    ])),
)
