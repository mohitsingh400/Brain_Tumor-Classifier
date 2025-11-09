"""
ML Model Loading and Prediction Module
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input as vgg_preprocess
import cv2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Class names - These should match the order used during training
# The model outputs predictions in the order: [glioma_tumor, meningioma_tumor, no_tumor, pituitary_tumor]
# This matches the alphabetical order of directory names used in flow_from_directory
CLASS_NAMES = ["glioma_tumor", "meningioma_tumor", "no_tumor", "pituitary_tumor"]
CLASS_NAMES_DISPLAY = {
    "glioma_tumor": "Glioma Tumor",
    "meningioma_tumor": "Meningioma Tumor",
    "no_tumor": "No Tumor",
    "pituitary_tumor": "Pituitary Tumor"
}

# Alternative class names (if model was trained differently)
# If predictions don't match, try uncommenting these and comment the above
# CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]
# CLASS_NAMES_DISPLAY = {
#     "glioma": "Glioma Tumor",
#     "meningioma": "Meningioma Tumor",
#     "notumor": "No Tumor",
#     "pituitary": "Pituitary Tumor"
# }

# Model paths - organized structure: models are stored in models/ directory
MODELS_DIR = os.path.join(BASE_DIR, "models")
CNN_MODEL_PATH = os.path.join(MODELS_DIR, "brain_tumor_cnn.h5")
VGG16_MODEL_PATH = os.path.join(MODELS_DIR, "brain_tumor_vgg16.h5")
# Fallback paths for backwards compatibility
CNN_MODEL_ALT = os.path.join(BASE_DIR, "brain_tumor_cnn.h5")
VGG16_MODEL_ALT = os.path.join(BASE_DIR, "brain_tumor_vgg16.h5")

# Load models (lazy loading)
_cnn_model = None
_vgg16_model = None

def load_cnn_model():
    """Load CNN model"""
    global _cnn_model
    if _cnn_model is None:
        model_path = None
        if os.path.exists(CNN_MODEL_PATH):
            model_path = CNN_MODEL_PATH
        elif os.path.exists(CNN_MODEL_ALT):
            model_path = CNN_MODEL_ALT
        
        if model_path:
            try:
                _cnn_model = load_model(model_path)
                print(f"CNN model loaded from {model_path}")
            except Exception as e:
                print(f"Error loading CNN model: {e}")
                raise Exception(f"Failed to load CNN model: {str(e)}")
        else:
            raise FileNotFoundError(f"CNN model not found. Checked: {CNN_MODEL_PATH}, {CNN_MODEL_ALT}")
    return _cnn_model

def load_vgg16_model():
    """Load VGG16 model"""
    global _vgg16_model
    if _vgg16_model is None:
        model_path = None
        if os.path.exists(VGG16_MODEL_PATH):
            model_path = VGG16_MODEL_PATH
        elif os.path.exists(VGG16_MODEL_ALT):
            model_path = VGG16_MODEL_ALT
        
        if model_path:
            try:
                _vgg16_model = load_model(model_path)
                print(f"VGG16 model loaded from {model_path}")
            except Exception as e:
                print(f"Error loading VGG16 model: {e}")
                raise Exception(f"Failed to load VGG16 model: {str(e)}")
        else:
            raise FileNotFoundError(f"VGG16 model not found. Checked: {VGG16_MODEL_PATH}, {VGG16_MODEL_ALT}")
    return _vgg16_model

def predict_cnn(image_path):
    """Predict using CNN model"""
    try:
        model = load_cnn_model()
        img = load_img(image_path, target_size=(150, 150))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        prediction = model.predict(img_array, verbose=0)[0]
        
        results = {}
        for i, cls in enumerate(CLASS_NAMES):
            results[CLASS_NAMES_DISPLAY[cls]] = float(prediction[i] * 100)
        
        predicted_index = np.argmax(prediction)
        predicted_class = CLASS_NAMES_DISPLAY[CLASS_NAMES[predicted_index]]
        confidence = float(prediction[predicted_index] * 100)
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'predictions': results,
            'model_type': 'CNN'
        }
    except Exception as e:
        raise Exception(f"CNN prediction error: {str(e)}")

def predict_vgg16(image_path):
    """Predict using VGG16 model"""
    try:
        model = load_vgg16_model()
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = vgg_preprocess(img_array)
        
        prediction = model.predict(img_array, verbose=0)[0]
        
        results = {}
        for i, cls in enumerate(CLASS_NAMES):
            results[CLASS_NAMES_DISPLAY[cls]] = float(prediction[i] * 100)
        
        predicted_index = np.argmax(prediction)
        predicted_class = CLASS_NAMES_DISPLAY[CLASS_NAMES[predicted_index]]
        confidence = float(prediction[predicted_index] * 100)
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'predictions': results,
            'model_type': 'VGG16'
        }
    except Exception as e:
        raise Exception(f"VGG16 prediction error: {str(e)}")

def predict_both(image_path):
    """Predict using both models"""
    cnn_result = predict_cnn(image_path)
    vgg16_result = predict_vgg16(image_path)
    return {
        'cnn': cnn_result,
        'vgg16': vgg16_result
    }

