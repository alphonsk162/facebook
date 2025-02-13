from .models import FriendRequest, Friendship, Post, Like, Comment
from django.db.models import Q
from django.contrib.auth.models import User
from user.models import UserDetails
from collections import deque
from feed.search_indexes import UserDetailsDocument


def find_friends(user_obj):
    friendship_objects = Friendship.objects.filter(
        Q(user1=user_obj) | Q(user2=user_obj)
    )
    friends_list = []
    for friendship_object in friendship_objects:
        if friendship_object.user1 != user_obj:
            friends_list.append(friendship_object.user1)
        else:
            friends_list.append(friendship_object.user2)
    return friends_list


def find_friends_dict(user_obj):
    friendship_objects = Friendship.objects.filter(
        Q(user1=user_obj) | Q(user2=user_obj)
    )
    friends_dict = {}
    for friendship_object in friendship_objects:
        if friendship_object.user1 != user_obj:
            friends_dict[friendship_object.user1] = True
        else:
            friends_dict[friendship_object.user2] = True
    return friends_dict


def find_searched_results(searched_name):
    users = UserDetails.objects.all()
    if len(searched_name) == 1:
        searched_name.append("")
    name_matching_objs = deque([])
    least_priority_name_matching_objects = []
    for user in users:
        if (
            searched_name[0].lower() in user.first_name.lower()
            and searched_name[1].lower() in user.last_name.lower()
        ):
            name_matching_objs.appendleft(user)
        elif searched_name[0].lower() in user.first_name.lower():
            name_matching_objs.append(user)
        elif searched_name[0].lower() in user.last_name.lower():
            least_priority_name_matching_objects.append(user)
    return list(name_matching_objs) + least_priority_name_matching_objects


def find_sent_friend_requests(from_user):
    sent_friend_requests = FriendRequest.objects.filter(from_user=from_user)
    sent_friend_requests_array = []
    for sent_friend_request in sent_friend_requests:
        sent_friend_requests_array.append(sent_friend_request.to_user.username)
    return sent_friend_requests_array


def find_received_friend_requests(to_user):
    received_friend_requests = FriendRequest.objects.filter(to_user=to_user)
    received_friend_requests_array = []
    for received_friend_request in received_friend_requests:
        received_friend_requests_array.append(
            received_friend_request.from_user.username
        )
    return received_friend_requests_array


def find_friends_post(user_obj):
    friends = find_friends_dict(user_obj)
    posts = Post.objects.all()
    posts_list = []
    for post in posts:
        if post.user in friends:
            posts_list.append(post)
    return posts_list


def posts_liked_by(user_obj):
    likes = Like.objects.all()
    posts = []
    for like in likes:
        if like.user == user_obj:
            posts.append(like.post)
    return posts


def find_parent_comments(post_obj):
    comments = Comment.objects.all()
    parent_comments = []
    for comment in comments:
        if comment.post.id == post_obj.id and comment.parent == None:
            parent_comments.append(comment)
    return parent_comments


def find_child_comments(parent_comments):
    child_comments_dict = {}
    child_comments = Comment.objects.filter(parent__isnull=False)
    for parent_comment in parent_comments:
        child_comments_dict[parent_comment] = []
    for child_comment in child_comments:
        if child_comment.parent in child_comments_dict:
            child_comments_dict[child_comment.parent].append(child_comment)
    return child_comments_dict


def find_user_posts(user_obj):
    posts = Post.objects.filter(user=user_obj)
    posts_array = []
    for post in posts:
        posts_array.append(post)
    return posts_array


def find_mutual_friends_count(user_obj1, user_obj2):
    user1_friends = find_friends(user_obj1)
    user2_friends = find_friends_dict(user_obj2)
    mutual_friends_count = 0
    for friend in user1_friends:
        if friend in user2_friends:
            mutual_friends_count += 1
    return mutual_friends_count


def search_users_by_name(name):
    results = UserDetailsDocument.search().query(
        "multi_match",
        query=name,
        fields=["full_name", "first_name", "last_name", "location"],
        fuzziness="AUTO",
    )
    return results
