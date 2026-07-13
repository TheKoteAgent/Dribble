from django.urls import path
from .views import (
    PublicUserProfileView,
    FollowToggleView, LikedShotsView, FollowersListView, FollowingListView
)

urlpatterns = [
    path('<str:username>/follow/', FollowToggleView.as_view(), name='follow_toggle'),
    path('<str:username>/liked/', LikedShotsView.as_view(), name='user_liked_shots'),
    path('<str:username>/followers/', FollowersListView.as_view(), name='user_followers'),
    path('<str:username>/following/', FollowingListView.as_view(), name='user_following'),
    path('<str:username>/', PublicUserProfileView.as_view(), name='public_user_profile'),
]

