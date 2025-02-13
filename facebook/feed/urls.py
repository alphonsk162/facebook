from django.urls import path
from .views import (
    home,
    profile,
    update_cover_photo,
    update_profile_photo,
    edit_profile,
    search_results,
    friend_requests,
    add_post,
    view_others_profile,
    comment_page,
    view_photos,
)

urlpatterns = [
    path("home/", home, name="home"),
    path("profile/", profile, name="profile"),
    path("update-cover-photo/", update_cover_photo, name="update_cover_photo"),
    path("update-profile-photo/", update_profile_photo, name="update_profile_photo"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("search-results/", search_results, name="search_results"),
    path("friend-requests/", friend_requests, name="friend_requests"),
    path("add-post/", add_post, name="add_post"),
    path("others-profile", view_others_profile, name="view_others_profile"),
    path("comment-page", comment_page, name="comment_page"),
    path("view-photos", view_photos, name="view_photos"),
]
