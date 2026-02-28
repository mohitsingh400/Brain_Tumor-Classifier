"""
Django Views for Brain Tumor Classifier
This module handles HTTP requests for image upload, prediction, and history viewing.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .models import Prediction
from .ml_model import run_prediction

def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def index(request):
    """
    Main page view - displays the image upload form.
    """
    return render(request, 'classifier/index.html')


@login_required
@require_http_methods(["POST"])
def predict(request):
    """
    Handle image upload and prediction.
    """
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    try:
        # Save uploaded image
        uploaded_file = request.FILES['image']
        file_name = default_storage.save(f'predictions/{uploaded_file.name}', uploaded_file)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        # Get request metadata
        model_type = request.POST.get('model_type', 'vgg16')
        patient_name = request.POST.get('patient_name', 'Anonymous')
        
        # Make prediction with Unified Function
        result = run_prediction(file_path, model_type)
        
        # Save prediction to database
        prediction_record = Prediction.objects.create(
            user=request.user,
            patient_name=patient_name,
            image=file_name,
            model_type=model_type,
            predicted_class=result['predicted_class'],
            confidence=result['confidence'],
            prediction_details=result['predictions']
        )
        
        # Return JSON response
        response_data = {
            'success': True,
            'prediction': result,
            'image_url': f'/media/{file_name}',
            'prediction_id': prediction_record.id
        }
        
        if 'gradcam_url' in result:
            response_data['gradcam_url'] = result['gradcam_url']
            
        return JsonResponse(response_data)
        
    except Exception as e:
        import traceback
        error_message = str(e)
        print(f"Prediction error: {error_message}")
        print(traceback.format_exc())
        return JsonResponse({'error': error_message}, status=500)


@login_required
@require_http_methods(["POST"])
def predict_vgg16(request):
    """Predict using VGG16 model only."""
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    try:
        uploaded_file = request.FILES['image']
        file_name = default_storage.save(f'predictions/{uploaded_file.name}', uploaded_file)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        result = run_prediction(file_path, "vgg16")
        
        prediction = Prediction.objects.create(
            user=request.user,
            patient_name=request.POST.get('patient_name', 'Anonymous'),
            image=file_name,
            model_type='vgg16',
            predicted_class=result['predicted_class'],
            confidence=result['confidence'],
            prediction_details=result['predictions']
        )
        
        response_data = {
            'success': True,
            'prediction': result,
            'image_url': f'/media/{file_name}',
            'prediction_id': prediction.id
        }
        
        if 'gradcam_url' in result:
            response_data['gradcam_url'] = result['gradcam_url']
            
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def predict_cnn(request):
    """Predict using CNN model only."""
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    try:
        uploaded_file = request.FILES['image']
        file_name = default_storage.save(f'predictions/{uploaded_file.name}', uploaded_file)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        result = run_prediction(file_path, "cnn")
        
        prediction = Prediction.objects.create(
            user=request.user,
            patient_name=request.POST.get('patient_name', 'Anonymous'),
            image=file_name,
            model_type='cnn',
            predicted_class=result['predicted_class'],
            confidence=result['confidence'],
            prediction_details=result['predictions']
        )
        
        response_data = {
            'success': True,
            'prediction': result,
            'image_url': f'/media/{file_name}',
            'prediction_id': prediction.id
        }
        
        if 'gradcam_url' in result:
            response_data['gradcam_url'] = result['gradcam_url']
            
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def history(request):
    """
    View prediction history page (only returning the user's history).
    """
    predictions = Prediction.objects.filter(user=request.user).order_by('-created_at')[:50]
    return render(request, 'classifier/history.html', {'predictions': predictions})


@login_required
def download_report(request, prediction_id):
    """
    Generate a downloadable PDF Medical AI report with Grad-CAM heatmaps.
    """
    prediction = get_object_or_404(Prediction, id=prediction_id, user=request.user)
    
    # Create the PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="brain_tumor_report_{prediction.patient_name}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Header styling
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Brain Tumor AI Classifier - Patient Diagnostic Report")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Patient Name: {prediction.patient_name}")
    p.drawString(50, height - 100, f"Technician: {prediction.user.username}")
    p.drawString(50, height - 120, f"Date: {prediction.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    p.line(50, height - 135, width - 50, height - 135)
    
    # Results Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 170, "Analysis Results")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 195, f"AI Diagnosis Focus: {prediction.predicted_class}")
    p.drawString(50, height - 215, f"Confidence Score: {prediction.confidence:.2f}%")
    p.drawString(50, height - 235, f"Analysis Model: {prediction.model_type.upper()}")
    
    # Embed Images
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 280, "Original MRI Scan:")
    p.drawString(320, height - 280, "Grad-CAM AI Focus (Heatsink):")
    
    try:
        # Original Image
        img_path = os.path.join(settings.MEDIA_ROOT, prediction.image.name)
        if os.path.exists(img_path):
            img_reader = ImageReader(img_path)
            p.drawImage(img_reader, 50, height - 500, width=220, height=200, preserveAspectRatio=True)
            
        # Grad-CAM Heatsink calculation
        gradcam_filename = prediction.image.name.replace('predictions/', 'gradcam/').replace('.jpg', '_cam.jpg').replace('.png', '_cam.jpg').replace('.jpeg', '_cam.jpg')
        gradcam_path = os.path.join(settings.MEDIA_ROOT, gradcam_filename)
        if os.path.exists(gradcam_path):
            grad_reader = ImageReader(gradcam_path)
            p.drawImage(grad_reader, 320, height - 500, width=220, height=200, preserveAspectRatio=True)
        else:
            p.setFont("Helvetica-Oblique", 10)
            p.drawString(320, height - 320, "Grad-CAM focus not generated for this scan.")
            
    except Exception as e:
        print(f"PDF Image Error: {e}")
        
    # Footer
    p.setFont("Helvetica", 9)
    p.drawString(50, 50, "Generated computationally by Deep Neural Networks. Not a substitute for professional medical advice.")
    p.showPage()
    p.save()
    
    return response

