# Brain Tumor AI Classifier - Project Structure & File Guide

This document provides a comprehensive breakdown of the project's directory structure and explains the specific purpose and functionality of every major file in the codebase.

## 📂 Root Directory (`/`)
- `manage.py`: The core Django command-line utility used to run the server, apply database migrations, and execute administrative tasks.
- `db.sqlite3`: The local SQLite database storing prediction history and user session data.
- `requirements.txt`: Lists all Python dependencies (e.g., Django, TensorFlow, OpenCV) required to run the project.
- `run_server.bat` / `run_server.sh`: Convenience scripts to quickly start the local development server on Windows or Unix systems.
- `README.md`: The primary entry point documentation explaining what the project is, how to install it, and basic usage.
- `ORGANIZATION_SUMMARY.md`: High-level summary of the project's organizational structure.

---

## 📂 `/brain_tumor_web/` (Django Configuration)
This folder contains the core settings for the entire Django project.
- `settings.py`: The most critical configuration file. It defines installed apps, database connection settings, static/media file routing (where images are saved), and security middleware.
- `urls.py`: The master URL router. It directs incoming web traffic to the appropriate app routing (connecting root domain to the `classifier` app).
- `wsgi.py` & `asgi.py`: Entrypoint configurations used by web servers (like Gunicorn or Daphne) to serve the application in production environments (synchronous and asynchronous).

---

## 📂 `/classifier/` (Main Application Logic)
This is where the actual functionality of the Brain Tumor Classifier lives.
- `ml_model.py`: **The Machine Learning Engine.** Contains the `run_prediction` function which acts as the single source of truth for both CNN and VGG16 models. It handles image preprocessing, confidence thresholding (Uncertainty logic), confidence capping, and generates the Grad-CAM explainability heatmaps using OpenCV.
- `views.py`: **The Controller.** Connects the frontend to the backend. It receives the uploaded image from the user, saves it to the database, calls the ML Engine (`ml_model.py`), and returns the JSON payload (predictions, Grad-CAM URLs) back to the frontend.
- `urls.py`: Maps specific web endpoints (like `/`, `/predict/`, `/history/`) to their corresponding functions in `views.py`.
- `models.py`: **The Database Schema.** Defines the `Prediction` table structure, tracking the image path, selected model, confidence score, predicted class, and timestamp for the history log.
- `admin.py`: Registers the database models so they can be viewed and managed in the Django Admin interface (`/admin/`).
- `apps.py`: Standard Django app configuration metadata.

### 📂 `/classifier/templates/classifier/` (HTML Views)
- `index.html`: The main web interface. Contains the drag-and-drop upload form, model selection toggles, and the responsive results dashboard for displaying original MRIs alongside Grad-CAM heatmaps.
- `history.html`: The prediction history page. Renders a grid of past analyses saved in the database.

### 📂 `/classifier/static/classifier/` (Frontend Assets)
- `js/main.js`: The frontend JavaScript logic. Intercepts form submissions, shows loading spinners, sends the image to the backend asynchronously (AJAX), and dynamically updates the DOM with the results and Grad-CAM images without reloading the page.
- `css/style.css`: The master stylesheet. Defines the premium "Medical AI" dark-themed aesthetic, glassmorphism card effects, typography (Inter/Outfit), and micro-animations.

---

## 📂 `/src/` & `/scripts/` (ML Training & Utilities)
Tools used for background machine learning tasks and project setup, independent of the active Django web server.
- `src/model.py`: Defines the neural network architectures (e.g., compiling the transfer learning layers for VGG16).
- `src/train.py`: The script used to originally parse the dataset and train the `.h5` model files.
- `src/test_and_explain.py`: A utility script for evaluating model accuracy on the test set and generating standalone Grad-CAM visualizations.
- `scripts/check_setup.py`: A debugging script to verify that TensorFlow, Django, and other dependencies are installed correctly.
- `scripts/download_data.py`: Automates the downloading and extraction of the brain tumor MRI dataset for training purposes.
- `scripts/comparison_plot.py`: Generates graphical charts comparing the performance of the CNN vs VGG16 models.
- `scripts/generate_report.py`: Aggregates model metrics and generates a PDF research report.

---

## 📂 `/models/` (Trained Weights)
- `brain_tumor_vgg16.h5`: The compiled weights for the VGG16 transfer learning model.
- `brain_tumor_cnn.h5`: The compiled weights for the custom Convolutional Neural Network.

---

## 📂 `/media/` (Dynamic Storage)
*Note: This folder is generated dynamically when the app runs.*
- `predictions/`: Stores the raw MRI images uploaded by the user.
- `gradcam/`: Stores the dynamically generated Grad-CAM heatmap overlays highlighting what the AI was looking at during inference.

---

## 📂 `/docs/` (Documentation)
Contains supporting reading material.
- `README_DJANGO.md`: Instructions specifically for setting up the Django backend.
- `QUICK_START.md`: A concise guide on how to boot up the project quickly.
- `TROUBLESHOOTING.md`: Common errors and their solutions.
- `PROJECT_STRUCTURE.md`: This architectural breakdown layout.
