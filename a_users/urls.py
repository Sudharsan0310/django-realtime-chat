from django.urls import path
from a_users.views import *

urlpatterns = [
    path("<str:username>/", profile_view, name="profile"),
    path('<username>/edit/', profile_edit_view, name="profile-edit"),
    path('<username>/onboarding/', profile_edit_view, name="profile-onboarding"),
    path('<username>/settings/', profile_settings_view, name="profile-settings"),
    path('<username>/emailchange/', profile_emailchange, name="profile-emailchange"),
    path('<username>/usernamechange/', profile_usernamechange, name="profile-usernamechange"),
    path('<username>/emailverify/', profile_emailverify, name="profile-emailverify"),
    path('<username>/delete/', profile_delete_view, name="profile-delete"),
]