from django.urls import path
from a_users.views import *

urlpatterns = [
    path('<str:username>/', profile_view, name="profile"),  # Fixed!
    path('<str:username>/edit/', profile_edit_view, name="profile-edit"),
    path('<str:username>/onboarding/', profile_edit_view, name="profile-onboarding"),
    path('<str:username>/settings/', profile_settings_view, name="profile-settings"),
    path('<str:username>/emailchange/', profile_emailchange, name="profile-emailchange"),
    path('<str:username>/usernamechange/', profile_usernamechange, name="profile-usernamechange"),
    path('<str:username>/emailverify/', profile_emailverify, name="profile-emailverify"),
    path('<str:username>/delete/', profile_delete_view, name="profile-delete"),
]