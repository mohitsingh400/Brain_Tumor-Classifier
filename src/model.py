"""
Model Architecture Definition
This module defines the VGG16-based transfer learning model for brain tumor classification.
The model uses a pre-trained VGG16 as a feature extractor with custom classification layers.
"""

from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam


def build_model(input_shape=(224, 224, 3), num_classes=4):
    """
    Build a transfer learning model using VGG16 for brain tumor classification.
    
    This function creates a model that:
    1. Uses pre-trained VGG16 (ImageNet weights) as a feature extractor
    2. Freezes the VGG16 base layers to prevent overfitting
    3. Adds custom classification layers on top
    
    Args:
        input_shape (tuple): Shape of input images (height, width, channels). Default: (224, 224, 3)
        num_classes (int): Number of tumor classes to classify. Default: 4
            - glioma_tumor
            - meningioma_tumor
            - no_tumor
            - pituitary_tumor
    
    Returns:
        tensorflow.keras.models.Sequential: Compiled model ready for training
    
    Example:
        >>> model = build_model(input_shape=(224, 224, 3), num_classes=4)
        >>> model.summary()
    """
    # Load pre-trained VGG16 model without top classification layer
    base_model = VGG16(weights="imagenet", include_top=False, input_shape=input_shape)
    
    # Freeze base model layers to prevent overfitting on small dataset
    # This allows us to use pre-learned features without retraining
    base_model.trainable = False

    # Build the complete model
    model = Sequential([
        base_model,                    # VGG16 feature extractor
        Flatten(),                     # Flatten feature maps to 1D
        Dense(256, activation="relu"), # Fully connected layer
        BatchNormalization(),          # Normalize activations
        Dropout(0.5),                  # Prevent overfitting (50% dropout)
        Dense(num_classes, activation="softmax")  # Output layer with softmax
    ])

    # Compile the model with appropriate optimizer and loss function
    model.compile(
        optimizer=Adam(learning_rate=1e-4),  # Adaptive learning rate optimizer
        loss="categorical_crossentropy",      # Multi-class classification loss
        metrics=["accuracy"]                  # Track accuracy during training
    )

    return model
