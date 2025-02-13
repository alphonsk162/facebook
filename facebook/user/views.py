from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.models import User
from .models import UserDetails
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

# from django.views.decorators.http import require_GET
# from .tasks import export_user_data

# Create your views here.


def login_page(request):
    return render(request, "user/login.html")


def signup_page(request):
    context = {"range": range(2025, 1904, -1)}
    return render(request, "user/signup.html", context)


def create_account(request):
    if request.POST:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")
        birth_day = int(request.POST.get("birth_day"))
        birth_month = int(request.POST.get("birth_month"))
        birth_year = int(request.POST.get("birth_year"))
        date_of_birth = datetime(
            year=birth_year, month=birth_month, day=birth_day
        ).date()
        gender = request.POST.get("gender")

        existing_emails = list(User.objects.values_list("email", flat=True))

        for existing_email in existing_emails:
            if email == existing_email:
                messages.error(
                    request,
                    "This email already exists. Please try using another email ID.",
                )
                return redirect("signup")
        if password != password2:
            messages.error(request, "Passwords did not match, Please try again.")
            return redirect("signup")
        else:
            messages.success(request, "Your Facebook account created successfully.")
            user = User.objects.create_user(
                username=email, password=password, email=email
            )
            UserDetails.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
            )
            return redirect("login")


def signin(request):
    if request.POST:
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email id or password")
            return redirect("login")


def signout(request):
    logout(request)
    return redirect("login")


# @require_GET
# def trigger_export(request):
#     """
#     View to trigger the export task
#     """
#     # Start the Celery task
#     task = export_user_data.delay()

#     return JsonResponse({"message": "Export started", "task_id": task.id})
