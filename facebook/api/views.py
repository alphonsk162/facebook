from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from feed.models import FriendRequest, Friendship, Post, Like, Comment, UserDetails
from rest_framework import status
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    to_user_id = request.data.get("to_user_id")
    print(to_user_id)
    if not to_user_id:
        return Response({"error": "Missing 'to_user_id'"}, status=400)
    try:
        to_user = User.objects.get(id=to_user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    print(to_user.profile.first_name)
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        return Response({"error": "Request already sent"}, status=400)

    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return Response({"status": "request_sent"})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_friend_request(request):
    to_user_id = request.data.get("to_user_id")
    to_user = User.objects.get(id=to_user_id)
    FriendRequest.objects.get(from_user=request.user, to_user=to_user).delete()
    return Response({"status": "request_cancelled"})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_friend_request(request):
    from_user_id = request.data.get("from_user_id")
    try:
        from_user = User.objects.get(id=from_user_id)
        FriendRequest.objects.filter(from_user=from_user, to_user=request.user).delete()
        Friendship.objects.get_or_create(user1=request.user, user2=from_user)
        return Response({"status": "friend_confirmed"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfriend(request):
    user_id = request.data.get("user_id")
    Friendship.objects.filter(user1=request.user, user2_id=user_id).delete()
    Friendship.objects.filter(user1_id=user_id, user2=request.user).delete()
    return Response({"status": "unfriended"})

@require_POST
@login_required
def toggle_like(request):
    post_id = request.POST.get('post_id')
    user = request.user

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    like, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    total_likes = Like.objects.filter(post=post).count()

    return JsonResponse({'liked': liked, 'total_likes': total_likes})


@require_POST
@login_required
def add_comment_or_reply(request):
    post_id = request.POST.get("post_id")
    content = request.POST.get("content")
    parent_id = request.POST.get("parent_id")
    reply_to = request.POST.get("reply_to", "")

    if not content:
        return JsonResponse({'error': 'Empty content'}, status=400)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
    user_profile = UserDetails.objects.get(user=request.user)

    comment = Comment.objects.create(
        post=post,
        user=request.user,
        user_profile=user_profile,
        content=content,
        parent=parent,
        reply_to=reply_to if parent else None,
    )

    return JsonResponse({
        'success': True,
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'reply_to': comment.reply_to,
            'user': user_profile.get_full_name(),
            'profile_pic': user_profile.profile_picture.url,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
            'is_reply': bool(parent),
            'parent_id': parent_id,
        }
    })
