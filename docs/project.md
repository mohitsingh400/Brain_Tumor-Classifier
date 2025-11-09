# Brain Tumor Classification Project

## Project Overview
This project is an **AI-powered brain tumor classification system** using **deep learning**. It leverages **VGG16 and custom CNN architectures** to classify brain MRI images into tumor categories.

The project demonstrates the **end-to-end pipeline**:
- Dataset downloading and preprocessing
- Model building, training, and evaluation
- Prediction and result visualization
- Reporting and comparison of results

---

## Features
- Uses **pre-trained VGG16 model** and custom CNN for classification.
- Supports **multi-class brain tumor classification**.
- Generates visual outputs for predictions.
- Modular and clean Python code for easy maintenance.
- Comprehensive results and reports stored in `results` and `reports` folders.

---

## Project Structure
brain_tumor/
│ brain_tumor_cnn.h5
│ check.py
│ download_data.py
│ project.md
│ Report_SubhashisBanerjee.pdf
│ requirements.txt
│
├───outputs/
│ └───figures/ # Generated visual outputs (plots, figures)
│
├───reports/ # Additional report files
│
├───results/
│ │ Brain_Tumor_Project_Report1.pdf
│ comp.py
│ comparision.png
│ make_report.py
│ prediction1.png
│ prediction2.png
│
├───src/
│ │ brain_tumor_vgg16.h5
│ │ model.py
│ │ predict.py
│ │ test_and_explain.py
│ │ train.py
│
└───Testing
│
└───Training


---

## Installation
1. Clone the repository:
```bash
git clone <your-repo-url>
cd brain_tumor

#Create a virtual environment (recommended):
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

#Download the dataset (if not included):
python download_data.py

#Train the model:
python src/train.py

#Make predictions on new images:
python src/predict.py --image <image_path>

#Test and explain model predictions:


#Generate reports:
python results/make_report.py

Outputs:-

Model weights: brain_tumor_cnn.h5, src/brain_tumor_vgg16.h5

Prediction visualizations: results/prediction1.png, results/prediction2.png

Comparative analysis: results/comparision.png

Project reports: results/Brain_Tumor_Project_Report.pdf, reports/

Future Enhancements

Integrate GUI (Streamlit or Flask) for live predictions.

Add real-time MRI prediction support.

Extend model to support more tumor types and larger datasets.

Implement explainable AI features for clinical use.