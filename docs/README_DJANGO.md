# Brain Tumor AI Classifier - Django Web Application

A beautiful, futuristic web interface for the Brain Tumor Classification system built with Django.

## Features

- 🎨 **Modern Futuristic UI** - Sleek design with animations and glassmorphism effects
- 🧠 **Dual Model Support** - Choose between CNN, VGG16, or compare both models
- 📊 **Real-time Predictions** - Instant analysis with detailed confidence scores
- 📈 **Visual Results** - Interactive charts and visualizations
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile devices
- 📝 **Prediction History** - View all previous predictions
- 🚀 **Fast & Efficient** - Optimized model loading and prediction

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd brain_tumor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create necessary directories:**
   ```bash
   mkdir -p media/predictions
   mkdir -p staticfiles
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

## Running the Application

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:8000/
   ```

## Usage

1. **Upload an Image:**
   - Click on the upload area or drag and drop a brain MRI image
   - Supported formats: JPG, PNG, JPEG (Max 10MB)

2. **Select Model:**
   - **VGG16**: Transfer learning model (~72% accuracy) - Recommended
   - **CNN**: Custom CNN model (~27% accuracy)
   - **Both**: Compare predictions from both models

3. **Analyze:**
   - Click "Analyze Image" button
   - Wait for the AI to process the image
   - View detailed results with confidence scores

4. **View History:**
   - Click "Prediction History" in the footer
   - View all previous predictions

## Model Requirements

Ensure you have the trained model files in one of these locations:
- `brain_tumor_cnn.h5` (root directory)
- `brain_tumor_vgg16.h5` (root directory)
- `src/brain_tumor_cnn.h5`
- `src/brain_tumor_vgg16.h5`

## Project Structure

```
brain_tumor/
├── brain_tumor_web/          # Django project settings
├── classifier/                # Main app
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── urls.py               # URL routing
│   ├── ml_model.py           # ML model integration
│   ├── templates/            # HTML templates
│   └── static/               # CSS, JS, images
├── media/                     # Uploaded files
├── staticfiles/               # Collected static files
└── manage.py                  # Django management script
```

## Admin Panel

Access the admin panel at:
```
http://127.0.0.1:8000/admin/
```

Login with your superuser credentials to manage predictions and view analytics.

## Troubleshooting

### Model Not Found Error
- Ensure model files (.h5) are in the correct location
- Check file permissions
- Verify model files are not corrupted

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings.py
- Ensure `DEBUG = True` for development

### Image Upload Issues
- Check file size (max 10MB)
- Verify image format (JPG, PNG, JPEG)
- Ensure `media/` directory has write permissions

## Technologies Used

- **Django 5.0** - Web framework
- **TensorFlow/Keras** - Machine learning
- **HTML5/CSS3** - Frontend design
- **JavaScript** - Interactive features
- **Font Awesome** - Icons
- **Google Fonts** - Typography (Orbitron, Exo 2)

## License

This project is part of a research project for brain tumor classification.

## Contact

For issues or questions, please refer to the main project documentation.

