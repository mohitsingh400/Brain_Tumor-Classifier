"""
Model Testing and Explanation Script
This script evaluates the model, generates confusion matrices, and creates Grad-CAM visualizations.
"""
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input as vgg_preprocess
ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "outputs" / "figures"
MODEL_DIR = ROOT / "models"  # Updated to models directory
TEST_DIR = ROOT / "data" / "Testing"  # Updated to data directory
os.makedirs(FIG_DIR, exist_ok=True)

CLASS_NAMES = None

# evaluate_model(model_path) - this function load model and test on dataset, also save confusion matrix
def evaluate_model(model_path):
    print("Loading model:", model_path)
    model = load_model(model_path)

    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    gen = ImageDataGenerator(preprocessing_function=vgg_preprocess)
    test_gen = gen.flow_from_directory(str(TEST_DIR), target_size=(224,224), batch_size=32, class_mode="categorical", shuffle=False)
    global CLASS_NAMES
    CLASS_NAMES = list(test_gen.class_indices.keys())
    preds = model.predict(test_gen, verbose=1)
    y_true = test_gen.classes
    y_pred = np.argmax(preds, axis=1)

    from sklearn.metrics import classification_report, confusion_matrix
    print(classification_report(y_true, y_pred, target_names=CLASS_NAMES))
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6,6))
    plt.imshow(cm)
    plt.title(f"Confusion: {Path(model_path).stem}")
    plt.colorbar()
    ticks = range(len(CLASS_NAMES))
    plt.xticks(ticks, CLASS_NAMES, rotation=45)
    plt.yticks(ticks, CLASS_NAMES)
    plt.tight_layout()
    out = FIG_DIR / f"{Path(model_path).stem}_confusion.png"
    plt.savefig(out, dpi=150)
    plt.close()
    return model, test_gen

# make_gradcam(model, img_path, last_conv_layer_name) - create gradcam heatmap on image
def make_gradcam(model, img_path, last_conv_layer_name=None):
    img = image.load_img(img_path, target_size=(224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = vgg_preprocess(x)

    if last_conv_layer_name is None:
        for layer in reversed(model.layers):
            if len(layer.output_shape) == 4:
                last_conv_layer_name = layer.name
                break

    grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(last_conv_layer_name).output, model.output])
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(x)
        pred_index = tf.argmax(predictions[0])
        loss = predictions[:, pred_index]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0,1,2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
    heatmap = heatmap.numpy()

    import cv2
    img_orig = cv2.imread(img_path)
    img_orig = cv2.resize(img_orig, (224,224))
    heatmap = cv2.resize(heatmap, (224,224))
    heatmap = np.uint8(255 * heatmap)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed = heatmap_color * 0.4 + img_orig * 0.6
    out_path = FIG_DIR / f"gradcam_{Path(img_path).stem}.jpg"
    cv2.imwrite(str(out_path), superimposed)
    return out_path

if __name__ == "__main__":
    # Look for model files in models/ directory
    candidates = ["brain_tumor_vgg16.h5", "brain_tumor_cnn.h5", 
                  "vgg16_transfer_finetune_final.keras", "vgg16_transfer_frozen_final.keras", "baseline_cnn_final.keras"]
    found = None
    for c in candidates:
        p = MODEL_DIR / c
        if p.exists():
            found = p
            break
    if found is None:
        # Fallback: search for any model files
        files = list(MODEL_DIR.glob("*.keras")) + list(MODEL_DIR.glob("*.h5"))
        if files:
            found = files[-1]
        else:
            raise FileNotFoundError(f"No trained model found in {MODEL_DIR}/")

    model, test_gen = evaluate_model(found)

    sample_paths = []
    base_test = TEST_DIR
    for cls in test_gen.class_indices.keys():
        cls_dir = base_test / cls
        imgs = list(cls_dir.glob("*.jpg"))[:2]
        for im in imgs:
            sample_paths.append(str(im))
            if len(sample_paths) >= 6:
                break
        if len(sample_paths) >= 6:
            break

    for p in sample_paths:
        out = make_gradcam(model, p)
        print("Saved gradcam:", out)

    print("Done. Grad-CAM images saved to:", FIG_DIR)
