# from celery import shared_task
# import json
# from django.core.serializers import serialize
# from .models import UserDetails
# from django.core.files.base import ContentFile
# from django.conf import settings
# import os
# from datetime import datetime


# @shared_task
# def export_user_data():
#     """
#     Celery task to export UserDetails data to JSON file
#     """
#     # Get all user details
#     data = serialize("json", UserDetails.objects.all())

#     # Create filename with timestamp
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"user_data_export_{timestamp}.json"

#     # Create exports directory if it doesn't exist
#     export_dir = os.path.join(settings.MEDIA_ROOT, "exports")
#     os.makedirs(export_dir, exist_ok=True)

#     # Save file
#     file_path = os.path.join(export_dir, filename)
#     with open(file_path, "w") as f:
#         f.write(data)

#     return file_path
