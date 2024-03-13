from django.urls import path

from learn_with_ease.web.views import main_page

urlpatterns = (
    path('', main_page, name='main_page'),
)