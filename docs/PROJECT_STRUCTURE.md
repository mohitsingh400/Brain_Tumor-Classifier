# Project Structure Guide

This document explains the organized structure of the Brain Tumor Classification project.

## Directory Organization

### `/brain_tumor_web/` - Django Project Settings
Contains Django project configuration files:
- `settings.py` - Django settings (database, installed apps, etc.)
- `urls.py` - Main URL routing configuration
- `wsgi.py` - WSGI configuration for deployment
- `asgi.py` - ASGI configuration for async support

### `/classifier/` - Main Django Application
The core Django app that handles the web interface:
- `models.py` - Database models (Prediction model)
- `views.py` - View functions (handle HTTP requests)
- `urls.py` - App-specific URL routing
- `ml_model.py` - ML model loading and prediction functions
- `admin.py` - Django admin configuration
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript)

### `/src/` - Machine Learning Source Code
Contains the core ML implementation:
- `model.py` - Model architecture definition (VGG16 transfer learning)
- `train.py` - Training script
- `predict.py` - Command-line prediction script
- `test_and_explain.py` - Model evaluation and Grad-CAM visualization

### `/scripts/` - Utility Scripts
Helper scripts for project management:
- `check_setup.py` - Verify installation and dependencies
- `download_data.py` - Download dataset from Kaggle
- `create_superuser.py` - Create Django admin user
- `comparison_plot.py` - Generate model comparison visualization
- `generate_report.py` - Generate PDF report

### `/models/` - Trained Model Files
Stores trained model weights:
- `brain_tumor_cnn.h5` - Custom CNN model
- `brain_tumor_vgg16.h5` - VGG16 transfer learning model

**Note:** Model files are large and should be stored separately or downloaded separately.

### `/data/` - Dataset
Organized dataset structure:
- `Training/` - Training images
  - `glioma_tumor/`
  - `meningioma_tumor/`
  - `no_tumor/`
  - `pituitary_tumor/`
- `Testing/` - Testing images
  - `glioma_tumor/`
  - `meningioma_tumor/`
  - `no_tumor/`
  - `pituitary_tumor/`

### `/media/` - User Uploads
Stores user-uploaded images for prediction:
- `predictions/` - Uploaded prediction images

### `/results/` - Analysis Results
Contains analysis outputs:
- `comparison.png` - Model comparison plot
- `prediction1.png`, `prediction2.png` - Prediction visualizations
- `Brain_Tumor_Project_Report1.pdf` - Project report

### `/outputs/` - Generated Outputs
Contains generated figures and outputs:
- `figures/` - Confusion matrices, Grad-CAM visualizations

### `/docs/` - Documentation
Project documentation:
- `README.md` - Main project documentation
- `project.md` - Project overview
- `README_DJANGO.md` - Django setup guide
- `QUICK_START.md` - Quick start guide
- `TROUBLESHOOTING.md` - Troubleshooting guide
- `PROJECT_STRUCTURE.md` - This file

### `/static/` - Static Files
Django static files (CSS, JavaScript, images)

## File Path Updates

All code files have been updated to use the new organized structure:

### Model Loading
- Models are loaded from `models/` directory
- Fallback to old locations for backwards compatibility

### Data Loading
- Training data: `data/Training/`
- Testing data: `data/Testing/`

### Script Execution
- All scripts can be run from project root
- Scripts automatically resolve correct paths

## Benefits of This Structure

1. **Organization**: Clear separation of concerns
2. **Maintainability**: Easy to find and update files
3. **Scalability**: Easy to add new features
4. **Clarity**: Self-documenting structure
5. **Best Practices**: Follows Django and Python project conventions

## Migration Notes

If you have an existing project:

1. **Model Files**: Move `.h5` files to `models/` directory
2. **Data**: Move `Training/` and `Testing/` to `data/` directory
3. **Scripts**: Move utility scripts to `scripts/` directory
4. **Documentation**: Move docs to `docs/` directory

The code has been updated to automatically check both old and new locations for backwards compatibility.

## Adding New Features

### Adding a New Model
1. Train the model using `src/train.py` or create new training script
2. Save model to `models/` directory
3. Update `classifier/ml_model.py` to load new model
4. Update views if needed

### Adding New Scripts
1. Create script in `scripts/` directory
2. Add proper documentation and comments
3. Update paths to use organized structure
4. Document in README.md

### Adding New Documentation
1. Create markdown file in `docs/` directory
2. Update main README.md with link
3. Follow existing documentation style

## Path Resolution

All scripts use relative path resolution:

```python
# Get project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get organized directories
models_dir = os.path.join(BASE_DIR, "models")
data_dir = os.path.join(BASE_DIR, "data")
scripts_dir = os.path.join(BASE_DIR, "scripts")
```

This ensures scripts work regardless of where they're called from.

## Questions?

Refer to:
- `README.md` - Main documentation
- `docs/TROUBLESHOOTING.md` - Common issues
- `docs/README_DJANGO.md` - Django-specific help

