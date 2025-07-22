from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from django.core.mail import send_mail
import os

# ✅ Register View (Sends Welcome Email directly, no Celery)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        user = serializer.save()

        # ✅ Send welcome email directly (no Celery)
        send_mail(
            subject="Welcome to Job Portal",
            message=f"Hello {user.username},\n\nThanks for registering with our portal!",
            from_email="yourgmail@gmail.com",  # Replace with your real email
            recipient_list=[user.email],
            fail_silently=False,
        )

# ✅ Resume Download View (no changes)
class ResumeDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.resume:
            return Response({"error": "No resume found"}, status=404)
        
        resume_path = request.user.resume.path
        if os.path.exists(resume_path):
            return FileResponse(open(resume_path, 'rb'), content_type='application/pdf')
        else:
            return Response({"error": "Resume file not found"}, status=404)
