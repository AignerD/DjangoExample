from django.shortcuts import render
from django.http import JsonResponse
import os
import datetime
import logging
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt

# Configure logging for the application
logging.basicConfig(
    filename=os.path.join(os.getcwd(), 'logs', 'recording_log.txt'),
    level=logging.INFO,
    format="%(asctime)s | IP: %(message)s | File: %(filename)s"
)

# Serve the frontend page
def home(request):
    return render(request, 'index.html')

# Function to get the user's IP address
def get_client_ip(request):
    """ Extracts the client IP address from request headers """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# ✅ CSRF-Exempt API to save the recorded audio file
@csrf_exempt
def save_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']

        # Extract user IP
        user_ip = get_client_ip(request)

        # Get current date and question number
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
        question_number = request.POST.get('question_number', 'Q1')  # Default to Q1 if not provided

        # Validate question number format
        if not question_number.startswith("Q") or not question_number[1:].isdigit():
            return JsonResponse({'error': 'Invalid question number format'}, status=400)

        # Construct the filename: IP_Date_Q#.wav
        file_name = f"{user_ip}_{current_date}_{question_number}.wav"

        # Define the storage path
        save_path = os.path.join('recordings', file_name)

        # Save the file
        path = default_storage.save(save_path, ContentFile(audio_file.read()))

        # ✅ Log the recording
        logging.info(f"{user_ip} | {file_name}")

        return JsonResponse({'message': 'Audio saved successfully', 'file_path': path, 'file_name': file_name})

    return JsonResponse({'error': 'Invalid request'}, status=400)
