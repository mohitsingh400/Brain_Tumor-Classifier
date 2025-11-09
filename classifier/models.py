"""
Database Models for Brain Tumor Classifier
This module defines the database models for storing prediction results.
"""

from django.db import models
import os
from django.conf import settings


class Prediction(models.Model):
    """
    Model to store brain tumor prediction results.
    
    This model stores:
    - The uploaded image
    - The model type used for prediction (CNN, VGG16, or Both)
    - The predicted tumor class
    - Confidence score
    - Detailed prediction probabilities for all classes
    - Timestamp of prediction
    """
    image = models.ImageField(upload_to='predictions/')
    model_type = models.CharField(
        max_length=50,
        choices=[
            ('cnn', 'CNN'),
            ('vgg16', 'VGG16'),
            ('both', 'Both'),
        ],
        default='vgg16'
    )
    predicted_class = models.CharField(max_length=50)  # e.g., "Glioma Tumor", "No Tumor"
    confidence = models.FloatField()  # Confidence score (0-100)
    prediction_details = models.JSONField(default=dict)  # Full prediction probabilities
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    class Meta:
        ordering = ['-created_at']  # Show newest predictions first

    def __str__(self):
        """String representation of the prediction"""
        return f"{self.predicted_class} ({self.confidence:.2f}%) - {self.created_at}"

