"""
Training Script for Brain Tumor Classification Model
This script trains a VGG16-based transfer learning model on brain tumor MRI images.
"""
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from model import build_model

# Set up paths - data is organized in data/ directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
train_dir = os.path.join(BASE_DIR, "data", "Training")
test_dir = os.path.join(BASE_DIR, "data", "Testing")
models_dir = os.path.join(BASE_DIR, "models")
os.makedirs(models_dir, exist_ok=True)  # Ensure models directory exists

print(f"Training dir: {train_dir}")
print(f"Testing dir: {test_dir}")

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest"
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224,224),
    batch_size=32,
    class_mode="categorical"
)

test_gen = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224,224),
    batch_size=32,
    class_mode="categorical"
)

# main train script - build model, train and save weights
model = build_model(input_shape=(224,224,3), num_classes=train_gen.num_classes)

history = model.fit(
    train_gen,
    epochs=20,
    validation_data=test_gen
)

# Save model to models/ directory
model_path = os.path.join(models_dir, "brain_tumor_vgg16.h5")
model.save(model_path)
print(f"Model saved to: {model_path}")
