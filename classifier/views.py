"""
Django Views for Brain Tumor Classifier
This module handles HTTP requests for image upload, prediction, and history viewing.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import json
from .models import Prediction
from .ml_model import predict_cnn, predict_vgg16, predict_both


def index(request):
    """
    Main page view - displays the image upload form.
    
    Returns:
        HttpResponse: Rendered index.html template
    """
    return render(request, 'classifier/index.html')


@require_http_methods(["POST"])
def predict(request):
    """
    Handle image upload and prediction.
    
    This view:
    1. Receives an uploaded image file
    2. Saves it to media/predictions/
    3. Runs prediction using selected model (CNN, VGG16, or Both)
    4. Saves prediction results to database
    5. Returns JSON response with prediction results
    
    Expected POST data:
        - image: Image file (required)
        - model_type: 'cnn', 'vgg16', or 'both' (optional, defaults to 'vgg16')
    
    Returns:
        JsonResponse: Prediction results with confidence scores
    """
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    try:
        # Save uploaded image
        uploaded_file = request.FILES['image']
        file_name = default_storage.save(f'predictions/{uploaded_file.name}', uploaded_file)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        # Get model type
        model_type = request.POST.get('model_type', 'vgg16')
        
        # Make prediction
        if model_type == 'cnn':
            result = predict_cnn(file_path)
        elif model_type == 'vgg16':
            result = predict_vgg16(file_path)
        elif model_type == 'both':
            # Predict with both models
            results = predict_both(file_path)
            result = {
                'predicted_class': results['vgg16']['predicted_class'],
                'confidence': results['vgg16']['confidence'],
                'predictions': results['vgg16']['predictions'],
                'model_type': 'Both',
                'cnn_result': results['cnn'],
                'vgg16_result': results['vgg16']
            }
        else:
            # Default to VGG16
            result = predict_vgg16(file_path)
        
        # Save prediction to database
        prediction = Prediction.objects.create(
            image=file_name,
            model_type=model_type,
            predicted_class=result['predicted_class'],
            confidence=result['confidence'],
            prediction_details=result['predictions']
        )
        
        # Return JSON response
        return JsonResponse({
            'success': True,
            'prediction': result,
            'image_url': f'/media/{file_name}',
            'prediction_id': prediction.id
        })
        
    except Exception as e:
        import traceback
        error_message = str(e)
        print(f"Prediction error: {error_message}")
        print(traceback.format_exc())
        return JsonResponse({'error': error_message}, status=500)

@require_http_methods(["POST"])
def predict_vgg16(request):
    """
    Predict using VGG16 model only.
    
    Returns:
        JsonResponse: VGG16 prediction results
    """
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    try:
        uploaded_file = request.FILES['image']
        file_name = default_storage.save(f'predictions/{uploaded_file.name}', uploaded_file)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        result = predict_vgg16(file_path)
        
        prediction = Prediction.objects.create(
            image=file_name,
            model_type='vgg16',
            predicted_class=result['predicted_class'],
            confidence=result['confidence'],
            prediction_details=result['predictions']
        )
        
        return JsonResponse({
            'success': True,
            'prediction': result,
            'image_url': f'/media/{file_name}',
            'prediction_id': prediction.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
def predict_cnn(request):
    """
    Predict using CNN model only.
    
    Returns:
        JsonResponse: CNN prediction results
    """
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    try:
        uploaded_file = request.FILES['image']
        file_name = default_storage.save(f'predictions/{uploaded_file.name}', uploaded_file)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        result = predict_cnn(file_path)
        
        prediction = Prediction.objects.create(
            image=file_name,
            model_type='cnn',
            predicted_class=result['predicted_class'],
            confidence=result['confidence'],
            prediction_details=result['predictions']
        )
        
        return JsonResponse({
            'success': True,
            'prediction': result,
            'image_url': f'/media/{file_name}',
            'prediction_id': prediction.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def history(request):
    """
    View prediction history page.
    
    Displays the last 50 predictions made by users.
    
    Returns:
        HttpResponse: Rendered history.html template with predictions
    """
    predictions = Prediction.objects.all()[:50]  # Last 50 predictions
    return render(request, 'classifier/history.html', {'predictions': predictions})

