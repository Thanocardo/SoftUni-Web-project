from django.urls import path, include

from learn_with_ease.user_profile.views import SignUpUserView, LoginUserView, sign_out_user, \
    ProfileView, ProfileUpdateView, ProfileDeleteView

urlpatterns = (
    path('register/', SignUpUserView.as_view(), name="profile_creation"),
    path('login/', LoginUserView.as_view(), name="login"),
    path('<slug:slug>/', include([
        path('edit', ProfileUpdateView.as_view(), name='profile_editing'),
        path('delete', ProfileDeleteView.as_view(), name='profile_delete'),
        path('', ProfileView.as_view(), name='profile'),
    ])),
    path('', sign_out_user, name='sign_out_user'),

)