# Quick Start Guide - Brain Tumor AI Classifier Web App

## 🚀 Quick Setup (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Run the Server
```bash
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser!

## 📋 Prerequisites

- Python 3.8+
- Trained model files:
  - `brain_tumor_cnn.h5` 
  - `brain_tumor_vgg16.h5`
  
  (These should be in the root directory or `src/` folder)

## 🎯 Features

✅ Drag & drop image upload  
✅ Real-time AI predictions  
✅ Beautiful futuristic UI  
✅ Model comparison (CNN vs VGG16)  
✅ Prediction history  
✅ Detailed confidence scores  

## 🖼️ Usage

1. **Upload** a brain MRI image
2. **Select** a model (VGG16 recommended)
3. **Click** "Analyze Image"
4. **View** results with confidence scores

## 🛠️ Troubleshooting

### Model Not Found
- Ensure `.h5` files are in root or `src/` directory
- Check file names match exactly

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Errors
```bash
python manage.py migrate
```

## 📝 Admin Access

Create superuser:
```bash
python manage.py createsuperuser
```

Access admin at: http://127.0.0.1:8000/admin/

## 🎨 UI Features

- Modern glassmorphism design
- Smooth animations
- Responsive layout
- Real-time predictions
- Interactive charts

Enjoy using the Brain Tumor AI Classifier! 🧠✨

