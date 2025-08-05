from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from user.models import UserDetails
from .models import FriendRequest, Friendship, Post, Like, Comment
from django.db.models import Q
from .helper_functions import (
    find_friends,
    find_searched_results,
    find_sent_friend_requests,
    find_received_friend_requests,
    find_friends_post,
    posts_liked_by,
    find_parent_comments,
    find_child_comments,
    find_user_posts,
    find_mutual_friends_count,
    search_users_by_name,
)


# Create your views here.
@login_required(login_url="login")
def home(request):
    if request.POST.get("like-post"):
        post = Post.objects.get(id=request.POST.get("like-post"))
        Like.objects.create(user=request.user, post=post)
        user_name = request.user
        user_obj = User.objects.get(username=user_name)
        user_profile = UserDetails.objects.get(user=user_obj)
        friends_user_obj = find_friends(user_obj)
        friends_list = []
        friends_post = find_friends_post(user_obj)
        liked_posts = posts_liked_by(user_name)
        for friend in friends_user_obj:
            friends_list.append(UserDetails.objects.get(user=friend))

        context = {
            "user_profile": user_profile,
            "friends_list": friends_list,
            "friends_post": friends_post,
            "liked_posts": liked_posts,
        }
        return redirect("home")

    elif request.POST.get("unlike-post"):
        Like.objects.get(
            user=request.user, post=request.POST.get("unlike-post")
        ).delete()
        user_name = request.user
        user_obj = User.objects.get(username=user_name)
        user_profile = UserDetails.objects.get(user=user_obj)
        friends_user_obj = find_friends(user_obj)
        friends_list = []
        friends_post = find_friends_post(user_obj)
        liked_posts = posts_liked_by(user_name)
        for friend in friends_user_obj:
            friends_list.append(UserDetails.objects.get(user=friend))

        context = {
            "user_profile": user_profile,
            "friends_list": friends_list,
            "friends_post": friends_post,
            "liked_posts": liked_posts,
        }
        return redirect("home")

    else:
        user_name = request.user
        user_obj = User.objects.get(username=user_name)
        user_profile = UserDetails.objects.get(user=user_obj)
        friends_user_obj = find_friends(user_obj)
        friends_list = []
        friends_post = find_friends_post(user_obj)
        liked_posts = posts_liked_by(user_name)
        for friend in friends_user_obj:
            friends_list.append(UserDetails.objects.get(user=friend))

        context = {
            "user_profile": user_profile,
            "friends_list": friends_list,
            "friends_post": friends_post,
            "liked_posts": liked_posts,
        }
        return render(request, "user/home.html", context)


@login_required(login_url="login")
def profile(request):
    user_name = request.user
    user = User.objects.get(username=user_name)
    user_profile = UserDetails.objects.get(user=user)
    full_name = user_profile.first_name + " " + user_profile.last_name
    friend_count = len(find_friends(user_name))
    context = {
        "user_profile": user_profile,
        "full_name": full_name,
        "friend_count": friend_count,
    }
    return render(request, "user/profile.html", context)


@login_required(login_url="login")
def update_cover_photo(request):
    if request.method == "POST" and request.FILES.get("cover_photo"):
        user_profile = UserDetails.objects.get(user=request.user)
        user_profile.cover_photo = request.FILES["cover_photo"]
        user_profile.save()
    return redirect("profile")


@login_required(login_url="login")
def update_profile_photo(request):
    if request.method == "POST" and request.FILES.get("profile_pic"):
        user_profile = UserDetails.objects.get(user=request.user)
        user_profile.profile_picture = request.FILES["profile_pic"]
        user_profile.save()
    return redirect("profile")


@login_required(login_url="login")
def edit_profile(request):
    user_name = request.user
    user = User.objects.get(username=user_name)
    user_profile = UserDetails.objects.get(user=user)
    works_at = request.POST.get("works_at")
    relationship_status = request.POST.get("relationship_status")
    lives_in = request.POST.get("lives_in")
    mobile_number = request.POST.get("mobile")
    if works_at != "":
        user_profile.works_at = works_at
    if relationship_status != "":
        user_profile.relationship_status = relationship_status
    if lives_in != "":
        user_profile.location = lives_in
    if mobile_number != "":
        user_profile.mobile_number = mobile_number
    user_profile.save()
    return redirect("profile")


@login_required(login_url="login")
def search_results(request):
    if request.POST.get("to_user_id") and request.POST.get("searched-name"):
        from_user = request.user
        to_user = User.objects.get(id=request.POST.get("to_user_id"))
        FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        searched_name = request.POST.get("searched-name").split(" ")
        users = UserDetails.objects.all()
        friends_list = find_friends(request.user)
        # search_results = search_users_by_name(
        #     request.POST.get("searched-name")
        # ).execute()
        # search_result_objects = []
        # for profile in search_results:
        #     search_result_objects.append(UserDetails.objects.get(id=profile.meta.id))
        context = {
            # "profiles": search_result_objects,
            "profiles": find_searched_results(searched_name),
            "searched_name": " ".join(searched_name),
            "sent_friend_requests": find_sent_friend_requests(request.user),
            "received_friend_requests": find_received_friend_requests(request.user),
            "friends_list": friends_list,
            "requesting_user": request.user,
        }
        return render(request, "user/search_results.html", context)

    elif request.POST.get("confirm_request") and request.POST.get("searched-name"):
        user1 = request.user
        user2 = User.objects.get(id=request.POST.get("confirm_request"))
        Friendship.objects.create(user1=user1, user2=user2)
        FriendRequest.objects.get(from_user=user2, to_user=user1).delete()
        searched_name = request.POST.get("searched-name").split(" ")
        users = UserDetails.objects.all()
        friends_list = find_friends(request.user)
        # search_result_objects = []
        # search_results = search_users_by_name(
        #     request.POST.get("searched-name")
        # ).execute()
        # for profile in search_results:
        #     search_result_objects.append(UserDetails.objects.get(id=profile.meta.id))
        context = {
            # "profiles": search_result_objects,
            "profiles": find_searched_results(searched_name),
            "searched_name": " ".join(searched_name),
            "sent_friend_requests": find_sent_friend_requests(request.user),
            "received_friend_requests": find_received_friend_requests(request.user),
            "friends_list": friends_list,
            "requesting_user": request.user,
        }
        return render(request, "user/search_results.html", context)

    elif request.POST.get("cancel_request") and request.POST.get("searched-name"):
        from_user = request.user
        to_user = User.objects.get(id=request.POST.get("cancel_request"))
        FriendRequest.objects.get(from_user=from_user, to_user=to_user).delete()
        searched_name = request.POST.get("searched-name").split(" ")
        friends_list = find_friends(request.user)
        # search_results = search_users_by_name(
        #     request.POST.get("searched-name")
        # ).execute()
        # search_result_objects = []
        # for profile in search_results:
        #     search_result_objects.append(UserDetails.objects.get(id=profile.meta.id))
        context = {
            # "profiles": search_result_objects,
            "profiles": find_searched_results(searched_name),
            "searched_name": " ".join(searched_name),
            "sent_friend_requests": find_sent_friend_requests(request.user),
            "received_friend_requests": find_received_friend_requests(request.user),
            "friends_list": friends_list,
            "requesting_user": request.user,
        }
        return render(request, "user/search_results.html", context)

    elif request.POST.get("unfriend") and request.POST.get("searched-name"):
        user1 = request.user
        user2 = User.objects.get(id=request.POST.get("unfriend"))
        friendship_obj = Friendship.objects.get(
            Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)
        ).delete()
        searched_name = request.POST.get("searched-name").split(" ")
        friends_list = find_friends(request.user)
        # search_results = search_users_by_name(
        #     request.POST.get("searched-name")
        # ).execute()
        # search_result_objects = []
        # for profile in search_results:
        #     search_result_objects.append(UserDetails.objects.get(id=profile.meta.id))
        context = {
            # "profiles": search_result_objects,
            "profiles": find_searched_results(searched_name),
            "searched_name": " ".join(searched_name),
            "sent_friend_requests": find_sent_friend_requests(request.user),
            "received_friend_requests": find_received_friend_requests(request.user),
            "friends_list": friends_list,
            "requesting_user": request.user,
        }
        return render(request, "user/search_results.html", context)

    else:
        searched_name = request.POST.get("searched-name").split(" ")
        users = UserDetails.objects.all()
        friends_list = find_friends(request.user)
        # search_results = search_users_by_name(
        #     request.POST.get("searched-name")
        # ).execute()
        # search_result_objects = []
        # for profile in search_results:
        #     search_result_objects.append(UserDetails.objects.get(id=profile.meta.id))
        context = {
            # "profiles": search_result_objects,
            "profiles": find_searched_results(searched_name),
            "searched_name": " ".join(searched_name),
            "sent_friend_requests": find_sent_friend_requests(request.user),
            "received_friend_requests": find_received_friend_requests(request.user),
            "friends_list": friends_list,
            "requesting_user": request.user,
        }
        return render(request, "user/search_results.html", context)


@login_required(login_url="login")
def friend_requests(request):
    if request.POST.get("from_user"):
        from_username = request.POST.get("from_user")
        to_user = request.user
        from_user = User.objects.get(username=from_username)
        FriendRequest.objects.filter(from_user=from_user, to_user=to_user).delete()
        user = request.user
        friend_requests = FriendRequest.objects.filter(to_user=user)
        friend_requests_array = []
        for friend_request in friend_requests:
            friend_requests_array.append(
                UserDetails.objects.get(user=friend_request.from_user)
            )
        context = {"friend_requests": friend_requests_array}
        return render(request, "user/friend_requests.html", context)

    elif request.POST.get("confirm_request_from_user"):
        from_username = request.POST.get("confirm_request_from_user")
        to_user = request.user
        from_user = User.objects.get(username=from_username)
        FriendRequest.objects.filter(to_user=to_user, from_user=from_user).delete()
        Friendship.objects.create(user1=from_user, user2=to_user)
        friend_requests = FriendRequest.objects.filter(to_user=request.user)
        friend_requests_array = []
        for friend_request in friend_requests:
            friend_requests_array.append(
                UserDetails.objects.get(user=friend_request.from_user)
            )
        context = {"friend_requests": friend_requests_array}
        return render(request, "user/friend_requests.html", context)

    else:
        user = request.user
        friend_requests = FriendRequest.objects.filter(to_user=user)
        friend_requests_array = []
        for friend_request in friend_requests:
            friend_requests_array.append(
                UserDetails.objects.get(user=friend_request.from_user)
            )
        context = {"friend_requests": friend_requests_array}
        return render(request, "user/friend_requests.html", context)


@login_required(login_url="login")
def add_post(request):
    user = request.user
    caption = request.POST.get("caption")
    post = Post.objects.create(user=user, caption=caption)
    post.image = request.FILES["post-image"]
    post.save()
    return redirect("profile")


@login_required(login_url="login")
def view_others_profile(request):
    user_details_obj = UserDetails.objects.get(user=request.user)
    if request.POST.get("profile-id") and user_details_obj.id == int(
        request.POST.get("profile-id")
    ):
        return redirect("profile")

    elif request.POST.get("to_user_id"):
        from_user = request.user
        to_user = User.objects.get(id=request.POST.get("to_user_id"))
        mutual_friends_count = find_mutual_friends_count(request.user, to_user)
        user_id = UserDetails.objects.get(user=to_user).id
        FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        users = UserDetails.objects.all()
        user_profile = UserDetails.objects.get(id=user_id)
        full_name = user_profile.first_name + " " + user_profile.last_name
        friend_count = len(find_friends(user_profile.user))
        friends_list = find_friends(request.user)
        context = {
            "profile": user_profile,
            "full_name": full_name,
            "friend_count": friend_count,
            "friends_list": friends_list,
            "sent_friend_requests": find_sent_friend_requests(request.user),
            "received_friend_requests": find_received_friend_requests(request.user),
            "mutual_friends_count": mutual_friends_count,
        }
        return render(request, "user/others_profile.html", context)
    elif request.POST.get("cancel_request"):
        from_user = request.user
        to_user = User.objects.get(id=request.POST.get("cancel_request"))
        mutual_friends_count = find_mutual_friends_count(request.user, to_user)
        FriendRequest.objects.get(from_user=from_user, to_user=to_user).delete()
        user_id = UserDetails.objects.get(user=to_user).id
        user_profile = UserDetails.objects.get(id=user_id)
        full_name = user_profile.first_name + " " + user_profile.last_name
        friend_count = len(find_friends(user_profile.user))
        friends_list = find_friends(request.user)
        context = {
            "profile": user_profile,
            "full_name": full_name,
            "friend_count": friend_count,
            "friends_list": friends_list,
            "sent_friend_requests": find_sent_friend_requests(request.user),
            "received_friend_requests": find_received_friend_requests(request.user),
            "mutual_friends_count": mutual_friends_count,
        }
        return render(request, "user/others_profile.html", context)

    elif request.POST.get("confirm_request"):
        user1 = request.user
        user2 = User.objects.get(id=request.POST.get("confirm_request"))
        mutual_friends_count = find_mutual_friends_count(request.user, user2)
        Friendship.objects.create(user1=user1, user2=user2)
        FriendRequest.objects.get(from_user=user2, to_user=user1).delete()
        user_id = UserDetails.objects.get(user=user2).id
        user_profile = UserDetails.objects.get(id=user_id)
        full_name = user_profile.first_name + " " + user_profile.last_name
        friend_count = len(find_friends(user_profile.user))
        friends_list = find_friends(request.user)
        context = {
            "profile": user_profile,
            "full_name": full_name,
            "friend_count": friend_count,
            "friends_list": friends_list,
            "sent_friend_requests": find_sent_friend_requests(request.user),
            "received_friend_requests": find_received_friend_requests(request.user),
            "mutual_friends_count": mutual_friends_count,
        }
        return render(request, "user/others_profile.html", context)

    elif request.POST.get("unfriend"):
        user1 = request.user
        user2 = User.objects.get(id=request.POST.get("unfriend"))
        mutual_friends_count = find_mutual_friends_count(request.user, user2)
        friendship_obj = Friendship.objects.get(
            Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)
        ).delete()
        user_id = UserDetails.objects.get(user=user2).id
        user_profile = UserDetails.objects.get(id=user_id)
        full_name = user_profile.first_name + " " + user_profile.last_name
        friend_count = len(find_friends(user_profile.user))
        friends_list = find_friends(request.user)
        context = {
            "profile": user_profile,
            "full_name": full_name,
            "friend_count": friend_count,
            "friends_list": friends_list,
            "sent_friend_requests": find_sent_friend_requests(request.user),
            "received_friend_requests": find_received_friend_requests(request.user),
            "mutual_friends_count": mutual_friends_count,
        }
        return render(request, "user/others_profile.html", context)

    else:
        user_id = request.POST.get("profile-id")
        user_profile = UserDetails.objects.get(id=user_id)
        full_name = user_profile.first_name + " " + user_profile.last_name
        friend_count = len(find_friends(user_profile.user))
        mutual_friends_count = find_mutual_friends_count(
            request.user, user_profile.user
        )
        print(mutual_friends_count)
        friends_list = find_friends(request.user)
        context = {
            "profile": user_profile,
            "full_name": full_name,
            "friend_count": friend_count,
            "friends_list": friends_list,
            "sent_friend_requests": find_sent_friend_requests(request.user),
            "received_friend_requests": find_received_friend_requests(request.user),
            "mutual_friends_count": mutual_friends_count,
        }
        return render(request, "user/others_profile.html", context)


def comment_page(request):
    if request.POST.get("add-comment"):
        comment_content = request.POST.get("add-comment")
        post_id = request.POST.get("post-id")
        post = Post.objects.get(id=post_id)
        user_details_obj = UserDetails.objects.get(user=request.user)
        Comment.objects.create(
            post=post,
            user=request.user,
            content=comment_content,
            user_profile=user_details_obj,
        )
        parent_comments = find_parent_comments(post)
        child_comments = find_child_comments(parent_comments)
        context = {
            "post": post,
            "parent_comments": parent_comments,
            "user_profile": user_details_obj,
            "child_comments": child_comments,
        }
        return render(request, "user/comments_page.html", context)

    elif request.POST.get("parent-id") and request.POST.get("add-reply"):
        comment_content = request.POST.get("add-reply")
        post_id = request.POST.get("post-id")
        parent_id = request.POST.get("parent-id")
        reply_to = request.POST.get("reply-to")
        user_details_obj = UserDetails.objects.get(user=request.user)
        post = Post.objects.get(id=post_id)
        parent_obj = Comment.objects.get(id=parent_id)
        Comment.objects.create(
            post=post,
            user=request.user,
            content=comment_content,
            user_profile=user_details_obj,
            parent=parent_obj,
            reply_to=reply_to,
        )
        post = Post.objects.get(id=post_id)
        parent_comments = find_parent_comments(post)
        child_comments = find_child_comments(parent_comments)
        user_details_obj = UserDetails.objects.get(user=request.user)
        context = {
            "post": post,
            "parent_comments": parent_comments,
            "user_profile": user_details_obj,
            "child_comments": child_comments,
        }
        return render(request, "user/comments_page.html", context)

    else:
        post_id = request.POST.get("view-comments")
        post = Post.objects.get(id=post_id)
        parent_comments = find_parent_comments(post)
        child_comments = find_child_comments(parent_comments)
        user_details_obj = UserDetails.objects.get(user=request.user)
        context = {
            "post": post,
            "parent_comments": parent_comments,
            "user_profile": user_details_obj,
            "child_comments": child_comments,
        }
        return render(request, "user/comments_page.html", context)


def view_photos(request):
    if request.POST.get("like-post"):
        post = Post.objects.get(id=request.POST.get("like-post"))
        Like.objects.create(user=request.user, post=post)
        user_name = request.user
        user_obj = User.objects.get(username=user_name)
        user_profile = UserDetails.objects.get(user=user_obj)
        friends_user_obj = find_friends(user_obj)
        user_posts = find_user_posts(user_obj)
        friends_post = find_friends_post(user_obj)
        liked_posts = posts_liked_by(user_name)
        friends_list = []
        for friend in friends_user_obj:
            friends_list.append(UserDetails.objects.get(user=friend))

        context = {
            "user_profile": user_profile,
            "friends_list": friends_list,
            "friends_post": user_posts,
            "liked_posts": liked_posts,
        }
        return redirect("view_photos")

    elif request.POST.get("unlike-post"):
        Like.objects.get(
            user=request.user, post=request.POST.get("unlike-post")
        ).delete()
        user_name = request.user
        user_obj = User.objects.get(username=user_name)
        user_profile = UserDetails.objects.get(user=user_obj)
        friends_user_obj = find_friends(user_obj)
        friends_list = []
        friends_post = find_friends_post(user_obj)
        liked_posts = posts_liked_by(user_name)
        for friend in friends_user_obj:
            friends_list.append(UserDetails.objects.get(user=friend))
        user_posts = find_user_posts(user_obj)
        context = {
            "user_profile": user_profile,
            "friends_list": friends_list,
            "friends_post": user_posts,
            "liked_posts": liked_posts,
        }
        return redirect("view_photos")

    elif request.POST.get("post-id"):
        print("FTVGYJ")
        Post.objects.get(id=request.POST.get("post-id")).delete()
        user_id = request.POST.get("user_id")
        user_name = request.user
        user_obj = User.objects.get(username=user_name)
        user_profile = UserDetails.objects.get(user=user_obj)
        friends_user_obj = find_friends(user_obj)
        friends_list = []
        friends_post = find_friends_post(user_obj)
        liked_posts = posts_liked_by(user_name)
        for friend in friends_user_obj:
            friends_list.append(UserDetails.objects.get(user=friend))

        user_posts = find_user_posts(user_obj)
        context = {
            "user_profile": user_profile,
            "friends_list": friends_list,
            "friends_post": user_posts,
            "liked_posts": liked_posts,
        }
        return render(request, "user/view_photos.html", context)

    else:
        user_id = request.POST.get("user_id")
        user_name = request.user
        user_obj = User.objects.get(username=user_name)
        user_profile = UserDetails.objects.get(user=user_obj)
        friends_user_obj = find_friends(user_obj)
        friends_list = []
        friends_post = find_friends_post(user_obj)
        liked_posts = posts_liked_by(user_name)
        for friend in friends_user_obj:
            friends_list.append(UserDetails.objects.get(user=friend))

        user_posts = find_user_posts(user_obj)
        context = {
            "user_profile": user_profile,
            "friends_list": friends_list,
            "friends_post": user_posts,
            "liked_posts": liked_posts,
        }
        return render(request, "user/view_photos.html", context)
