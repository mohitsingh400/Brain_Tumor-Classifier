// Main JavaScript for Brain Tumor Classifier

document.addEventListener('DOMContentLoaded', function () {
    const uploadArea = document.getElementById('uploadArea');
    const imageInput = document.getElementById('imageInput');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const removeImageBtn = document.getElementById('removeImage');
    const uploadForm = document.getElementById('uploadForm');
    const predictBtn = document.getElementById('predictBtn');
    const btnLoader = document.getElementById('btnLoader');
    const btnText = predictBtn.querySelector('.btn-text');
    const resultsSection = document.getElementById('resultsSection');
    const closeResultsBtn = document.getElementById('closeResults');
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notificationText');

    // File upload handling
    uploadArea.addEventListener('click', () => imageInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('dragleave', handleDragLeave);

    imageInput.addEventListener('change', handleFileSelect);
    removeImageBtn.addEventListener('click', removeImage);

    // Form submission
    uploadForm.addEventListener('submit', handleFormSubmit);

    // Close results
    closeResultsBtn.addEventListener('click', () => {
        resultsSection.style.display = 'none';
    });

    function handleDragOver(e) {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.background = 'rgba(0, 212, 255, 0.15)';
    }

    function handleDragLeave(e) {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border-color)';
        uploadArea.style.background = 'rgba(0, 212, 255, 0.05)';
    }

    function handleDrop(e) {
        e.preventDefault();
        handleDragLeave(e);
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }

    function handleFile(file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            showNotification('Please select an image file', 'error');
            return;
        }

        // Validate file size (10MB)
        if (file.size > 10 * 1024 * 1024) {
            showNotification('File size should be less than 10MB', 'error');
            return;
        }

        // Create preview
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            previewContainer.style.display = 'block';
            uploadArea.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    function removeImage() {
        imageInput.value = '';
        previewContainer.style.display = 'none';
        uploadArea.style.display = 'block';
    }

    async function handleFormSubmit(e) {
        e.preventDefault();

        if (!imageInput.files || imageInput.files.length === 0) {
            showNotification('Please select an image', 'error');
            return;
        }

        const formData = new FormData(uploadForm);
        const modelType = formData.get('model_type');

        // Disable button and show loading
        predictBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';

        try {
            const response = await fetch('/predict/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            const data = await response.json();

            if (data.success) {
                displayResults(data);
                showNotification('Analysis completed successfully!', 'success');
            } else {
                showNotification(data.error || 'An error occurred', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('Network error. Please try again.', 'error');
        } finally {
            // Re-enable button
            predictBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
        }
    }

    function displayResults(data) {
        const prediction = data.prediction;

        // Expose Download Report PDF button
        const downloadReportBtn = document.getElementById('downloadReportBtn');
        if (downloadReportBtn && data.prediction_id) {
            downloadReportBtn.href = `/download-report/${data.prediction_id}/`;
            downloadReportBtn.style.display = 'inline-block';
        }

        // Display main prediction
        document.getElementById('className').textContent = prediction.predicted_class;
        document.getElementById('confidenceText').textContent = `${prediction.confidence.toFixed(2)}%`;

        // Animate confidence bar
        const confidenceFill = document.getElementById('confidenceFill');
        confidenceFill.style.width = '0%';
        setTimeout(() => {
            confidenceFill.style.width = `${prediction.confidence}%`;
        }, 100);

        // Display predictions breakdown
        const predictionsList = document.getElementById('predictionsList');
        predictionsList.innerHTML = '';

        // Sort predictions by confidence
        const sortedPredictions = Object.entries(prediction.predictions)
            .sort((a, b) => b[1] - a[1]);

        sortedPredictions.forEach(([className, confidence], index) => {
            const item = document.createElement('div');
            item.className = 'prediction-item';
            item.innerHTML = `
                <span class="prediction-item-name">${className}</span>
                <div class="prediction-item-bar">
                    <div class="prediction-item-fill" style="width: 0%"></div>
                </div>
                <span class="prediction-item-percent">${confidence.toFixed(2)}%</span>
            `;
            predictionsList.appendChild(item);

            // Animate bar
            setTimeout(() => {
                const fill = item.querySelector('.prediction-item-fill');
                fill.style.width = `${confidence}%`;
            }, 200 + (index * 100));
        });

        // Display uploaded image
        document.getElementById('resultImage').src = data.image_url;

        // Display Grad-CAM if available
        const gradcamContainer = document.getElementById('gradcamContainer');
        const gradcamImage = document.getElementById('gradcamImage');
        if (data.gradcam_url && gradcamContainer && gradcamImage) {
            gradcamImage.src = data.gradcam_url;
            gradcamContainer.style.display = 'block';
        } else if (gradcamContainer) {
            gradcamContainer.style.display = 'none';
        }

        // Display model comparison if both models were used
        if (prediction.cnn_result && prediction.vgg16_result) {
            const comparisonSection = document.getElementById('modelComparison');
            const comparisonGrid = document.getElementById('comparisonGrid');

            comparisonGrid.innerHTML = `
                <div class="comparison-card">
                    <h4>CNN Model</h4>
                    <p><strong>Prediction:</strong> ${prediction.cnn_result.predicted_class}</p>
                    <p><strong>Confidence:</strong> ${prediction.cnn_result.confidence.toFixed(2)}%</p>
                </div>
                <div class="comparison-card">
                    <h4>VGG16 Model</h4>
                    <p><strong>Prediction:</strong> ${prediction.vgg16_result.predicted_class}</p>
                    <p><strong>Confidence:</strong> ${prediction.vgg16_result.confidence.toFixed(2)}%</p>
                </div>
            `;

            comparisonSection.style.display = 'block';
        } else {
            document.getElementById('modelComparison').style.display = 'none';
        }

        // Show results section
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function showNotification(message, type = 'info') {
        notificationText.textContent = message;
        notification.className = `notification show ${type}`;

        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

