"""
ML Model Loading and Prediction Module
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import cv2
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Class names - These should match the order used during training
CLASS_NAMES = ["glioma_tumor", "meningioma_tumor", "no_tumor", "pituitary_tumor"]
CLASS_NAMES_DISPLAY = {
    "glioma_tumor": "Glioma Tumor",
    "meningioma_tumor": "Meningioma Tumor",
    "no_tumor": "No Tumor",
    "pituitary_tumor": "Pituitary Tumor"
}

# Model paths
MODELS_DIR = os.path.join(BASE_DIR, "models")
CNN_MODEL_PATH = os.path.join(MODELS_DIR, "brain_tumor_cnn.h5")
VGG16_MODEL_PATH = os.path.join(MODELS_DIR, "brain_tumor_vgg16.h5")
CNN_MODEL_ALT = os.path.join(BASE_DIR, "brain_tumor_cnn.h5")
VGG16_MODEL_ALT = os.path.join(BASE_DIR, "brain_tumor_vgg16.h5")

# Load models (lazy loading)
_cnn_model = None
_vgg16_model = None

def load_cnn_model():
    """Load CNN model"""
    global _cnn_model
    if _cnn_model is None:
        model_path = CNN_MODEL_PATH if os.path.exists(CNN_MODEL_PATH) else CNN_MODEL_ALT
        if os.path.exists(model_path):
            try:
                _cnn_model = load_model(model_path)
            except Exception as e:
                raise Exception(f"Failed to load CNN model: {str(e)}")
        else:
            raise FileNotFoundError("CNN model not found.")
    return _cnn_model

def load_vgg16_model():
    """Load VGG16 model"""
    global _vgg16_model
    if _vgg16_model is None:
        model_path = VGG16_MODEL_PATH if os.path.exists(VGG16_MODEL_PATH) else VGG16_MODEL_ALT
        if os.path.exists(model_path):
            try:
                _vgg16_model = load_model(model_path)
            except Exception as e:
                raise Exception(f"Failed to load VGG16 model: {str(e)}")
        else:
            raise FileNotFoundError("VGG16 model not found.")
    return _vgg16_model

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    """Generate Grad-CAM heatmap for a model."""
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def save_gradcam(image_path, heatmap, cam_path="cam_img.jpg", alpha=0.4):
    """Superimpose Grad-CAM heatmap on original image."""
    img = cv2.imread(image_path)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    superimposed_img = heatmap * alpha + img
    cv2.imwrite(cam_path, superimposed_img)

def run_prediction(image_path, model_type="vgg16"):
    """
    Single source of truth for predictions.
    Handles CNN and VGG16, handles bounds of prediction, confidence caps, and preprocessing uniformities.
    """
    try:
        if model_type.lower() == "cnn":
            model = load_cnn_model()
            target_size = (150, 150)
            # Find last conv layer dynamically for CNN. Usually max_pooling2d or conv2d
            last_conv_layer = [layer.name for layer in model.layers if 'conv' in layer.name.lower() or 'pool' in layer.name.lower()][-1]
        elif model_type.lower() == "vgg16":
            model = load_vgg16_model()
            target_size = (224, 224)
            # VGG16 specific last active conv layer
            last_conv_layer = "block5_conv3"
        elif model_type.lower() == "both":
            cnn_result = run_prediction(image_path, "cnn")
            vgg16_result = run_prediction(image_path, "vgg16")
            
            # The 'both' route returns mainly VGG16 payload wrapping both.
            return {
                'predicted_class': vgg16_result['predicted_class'],
                'confidence': vgg16_result['confidence'],
                'predictions': vgg16_result['predictions'],
                'model_type': 'Both',
                'cnn_result': cnn_result,
                'vgg16_result': vgg16_result,
                'gradcam_url': vgg16_result.get('gradcam_url', '')
            }
        else:
            raise ValueError(f"Unknown model_type {model_type}")

        # Uniform preprocessing
        img = load_img(image_path, target_size=target_size)
        img_array = img_to_array(img) / 255.0
        batch_array = np.expand_dims(img_array, axis=0)

        raw_prediction = model.predict(batch_array, verbose=0)[0]
        
        # Calculate confidences
        results = {}
        for i, cls in enumerate(CLASS_NAMES):
            val = float(raw_prediction[i] * 100)
            results[CLASS_NAMES_DISPLAY[cls]] = val
        
        predicted_index = int(np.argmax(raw_prediction))
        predicted_class = CLASS_NAMES_DISPLAY[CLASS_NAMES[predicted_index]]
        confidence = float(raw_prediction[predicted_index] * 100)

        # Enforce Minimum Confidence Rule and Upper Confidence Cap rules
        if confidence < 60.0:
            predicted_class = "Uncertain"
        
        if confidence > 95.0:
            confidence = 95.0

        gradcam_url = None
        # Generate Grad-CAM output
        try:
            heatmap = make_gradcam_heatmap(batch_array, model, last_conv_layer, predicted_index)
            # Save absolute path to django media directory structure correctly alongside original inference images
            media_dir = os.path.dirname(image_path)
            cam_filename = f"cam_{uuid.uuid4().hex[:8]}.jpg"
            cam_path = os.path.join(media_dir, cam_filename)
            save_gradcam(image_path, heatmap, cam_path)
            
            # Since our images go to media/predictions/, we return that prefix relative path for django context
            if "media" in cam_path:
                rel_path = cam_path.split("media")[-1].replace("\\", "/")
                gradcam_url = f"/media{rel_path}"
        except Exception as e:
            print(f"Failed to generate Grad-CAM: {e}")

        payload = {
            'predicted_class': predicted_class,
            'confidence': round(confidence, 2),
            'predictions': results,
            'model_type': model_type.upper()
        }
        if gradcam_url:
            payload['gradcam_url'] = gradcam_url

        return payload

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise Exception(f"Prediction error ({model_type}): {str(e)}")
