# Brain Tumor Classification System

An AI-powered brain tumor classification system using deep learning, built with Django for web interface and TensorFlow/Keras for machine learning models.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Training](#model-training)
- [Web Application](#web-application)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This project implements a brain tumor classification system that can classify brain MRI images into four categories:
- **Glioma Tumor**
- **Meningioma Tumor**
- **No Tumor**
- **Pituitary Tumor**

The system uses two different models:
1. **Custom CNN** - A baseline convolutional neural network
2. **VGG16 Transfer Learning** - A pre-trained VGG16 model with transfer learning (Recommended)

## ✨ Features

### Machine Learning
- ✅ VGG16 transfer learning model (~72% accuracy)
- ✅ Custom CNN baseline model (~27% accuracy)
- ✅ Model comparison and evaluation
- ✅ Grad-CAM visualization for model explainability
- ✅ Confusion matrix generation

### Web Application
- 🎨 Modern, futuristic UI with glassmorphism effects
- 📊 Real-time predictions with confidence scores
- 📈 Interactive visualizations
- 📱 Responsive design (desktop, tablet, mobile)
- 📝 Prediction history tracking
- 🚀 Fast and efficient model loading

## 📁 Project Structure

```
brain_tumor/
├── brain_tumor_web/          # Django project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI configuration
│
├── classifier/                # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── urls.py               # App URL routing
│   ├── ml_model.py           # ML model integration
│   ├── templates/            # HTML templates
│   │   └── classifier/
│   │       ├── index.html    # Main prediction page
│   │       └── history.html  # Prediction history
│   └── static/               # Static files (CSS, JS)
│       └── classifier/
│
├── src/                       # Machine learning source code
│   ├── model.py              # Model architecture definition
│   ├── train.py              # Training script
│   ├── predict.py            # Prediction script
│   └── test_and_explain.py   # Model evaluation & Grad-CAM
│
├── scripts/                   # Utility scripts
│   ├── check_setup.py        # Setup verification
│   ├── download_data.py      # Dataset download
│   ├── create_superuser.py   # Django superuser creation
│   ├── comparison_plot.py    # Model comparison visualization
│   └── generate_report.py    # PDF report generation
│
├── models/                    # Trained model files
│   ├── brain_tumor_cnn.h5    # CNN model weights
│   └── brain_tumor_vgg16.h5  # VGG16 model weights
│
├── data/                      # Dataset
│   ├── Training/             # Training images
│   │   ├── glioma_tumor/
│   │   ├── meningioma_tumor/
│   │   ├── no_tumor/
│   │   └── pituitary_tumor/
│   └── Testing/              # Testing images
│       ├── glioma_tumor/
│       ├── meningioma_tumor/
│       ├── no_tumor/
│       └── pituitary_tumor/
│
├── media/                     # User-uploaded files
│   └── predictions/          # Prediction images
│
├── results/                   # Analysis results
│   ├── comparison.png        # Model comparison plot
│   ├── prediction1.png       # Prediction visualization
│   ├── prediction2.png       # Prediction visualization
│   └── Brain_Tumor_Project_Report1.pdf
│
├── outputs/                   # Generated outputs
│   └── figures/              # Confusion matrices, Grad-CAM
│
├── docs/                      # Documentation
│   ├── project.md            # Project overview
│   ├── README_DJANGO.md      # Django setup guide
│   ├── QUICK_START.md        # Quick start guide
│   └── TROUBLESHOOTING.md    # Troubleshooting guide
│
├── static/                    # Static files
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── db.sqlite3                 # SQLite database
└── README.md                  # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd brain_tumor
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Setup

```bash
python scripts/check_setup.py
```

This will check if all dependencies are installed correctly and if model files are present.

### Step 5: Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

```bash
python scripts/create_superuser.py
```

Or use Django's built-in command:

```bash
python manage.py createsuperuser
```

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## 💻 Usage

### Running the Web Application

1. **Start the development server:**

```bash
python manage.py runserver
```

2. **Open your browser and navigate to:**

```
http://127.0.0.1:8000/
```

3. **Upload an image and make predictions:**
   - Click on the upload area or drag and drop a brain MRI image
   - Select a model (VGG16 recommended)
   - Click "Analyze Image"
   - View results with confidence scores

### Using Command Line Tools

#### Make Predictions

```bash
python src/predict.py <image_path>
```

#### Train Model

```bash
python src/train.py
```

#### Evaluate Model and Generate Grad-CAM

```bash
python src/test_and_explain.py
```

#### Generate Comparison Plot

```bash
python scripts/comparison_plot.py
```

#### Generate Report

```bash
python scripts/generate_report.py
```

## 🎓 Model Training

### Download Dataset

```bash
python scripts/download_data.py
```

This will download the dataset to the `data/` directory. You may need to organize the files into `Training/` and `Testing/` subdirectories.

### Train the Model

```bash
cd src
python train.py
```

The trained model will be saved to `models/brain_tumor_vgg16.h5`.

### Model Architecture

The VGG16 transfer learning model:
- Uses pre-trained VGG16 (ImageNet weights) as feature extractor
- Freezes base layers to prevent overfitting
- Adds custom classification layers:
  - Flatten layer
  - Dense(256, ReLU)
  - BatchNormalization
  - Dropout(0.5)
  - Dense(4, Softmax) - 4 tumor classes

### Training Parameters

- **Input size:** 224x224 pixels
- **Batch size:** 32
- **Epochs:** 20
- **Optimizer:** Adam (learning rate: 1e-4)
- **Loss:** Categorical crossentropy
- **Data augmentation:** Rotation, shift, shear, zoom, flip

## 🌐 Web Application

### Features

- **Image Upload:** Drag & drop or click to upload
- **Model Selection:** Choose between CNN, VGG16, or both
- **Real-time Prediction:** Instant results with confidence scores
- **Prediction History:** View all previous predictions
- **Admin Panel:** Manage predictions and view analytics

### Access Admin Panel

```
http://127.0.0.1:8000/admin/
```

Login with your superuser credentials.

## 📚 Documentation

Additional documentation is available in the `docs/` directory:

- **project.md** - Detailed project overview and methodology
- **README_DJANGO.md** - Django-specific setup and usage
- **QUICK_START.md** - Quick start guide
- **TROUBLESHOOTING.md** - Common issues and solutions

## 🔧 Troubleshooting

### Model Not Found Error

- Ensure model files (.h5) are in the `models/` directory
- Check file names match exactly: `brain_tumor_cnn.h5`, `brain_tumor_vgg16.h5`
- Verify file permissions

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

Check `STATIC_URL` and `STATIC_ROOT` in `brain_tumor_web/settings.py`.

### Database Errors

```bash
python manage.py migrate
```

### Image Upload Issues

- Check file size (max 10MB)
- Verify image format (JPG, PNG, JPEG)
- Ensure `media/` directory has write permissions

### Dependencies Issues

```bash
pip install --upgrade -r requirements.txt
```

## 🛠️ Technologies Used

### Backend
- **Django 5.0** - Web framework
- **TensorFlow 2.20** - Machine learning framework
- **Keras 3.11** - Deep learning API
- **NumPy** - Numerical computing
- **Pillow** - Image processing
- **OpenCV** - Computer vision

### Frontend
- **HTML5/CSS3** - Markup and styling
- **JavaScript** - Interactive features
- **Font Awesome** - Icons
- **Google Fonts** - Typography (Orbitron, Exo 2)

### Data Science
- **Matplotlib** - Plotting and visualization
- **Scikit-learn** - Machine learning utilities
- **Pandas** - Data manipulation

## 📊 Model Performance

| Model | Training Accuracy | Validation Accuracy |
|-------|------------------|---------------------|
| Custom CNN | 39% | 27% |
| VGG16 Transfer Learning | 89% | 72% |

**Recommendation:** Use VGG16 model for better accuracy and generalization.

## 📝 License

This project is part of a research project for brain tumor classification.

## 👥 Contributors

- Subhashis Banerjee

## 🙏 Acknowledgments

- Dataset: [Brain Tumor Classification (MRI)](https://www.kaggle.com/datasets/sartajbhuvaji/brain-tumor-classification-mri) on Kaggle
- VGG16: Pre-trained on ImageNet
- Django Community

## 📞 Support

For issues or questions, please refer to:
- `docs/TROUBLESHOOTING.md` for common issues
- `docs/README_DJANGO.md` for Django-specific help
- Project documentation in `docs/` directory

## 🔮 Future Enhancements

- [ ] Integrate additional pre-trained models (ResNet, Inception)
- [ ] Add real-time MRI prediction support
- [ ] Extend to support more tumor types
- [ ] Implement explainable AI features for clinical use
- [ ] Add model ensemble predictions
- [ ] Deploy to cloud platform
- [ ] Add REST API endpoints
- [ ] Implement user authentication
- [ ] Add batch prediction support

---

**Note:** This project is for research and educational purposes. For medical diagnosis, please consult healthcare professionals.

