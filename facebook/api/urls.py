from django.urls import path
from . import views

urlpatterns = [
    path("friend-request/send/", views.send_friend_request),
    path("friend-request/cancel/", views.cancel_friend_request),
    path("friend-request/confirm/", views.confirm_friend_request),
    path("friend-request/unfriend/", views.unfriend),
    path('toggle-like/', views.toggle_like, name='toggle-like'),
    path('add-comment/', views.add_comment_or_reply, name='add-comment'),
]
