 Smart Crop Health and Disease Recommendation 

A Flask-based web application that detects potato leaf diseases from uploaded images using a MobileNetV2-based CNN model, and provides instant treatment recommendations — with real-time weather-based advisory and an admin dashboard to track prediction history.

---

📌 Overview

This system allows a user to upload a photo of a potato leaf through a simple web interface. The image is validated, analyzed by a deep learning model, and classified into one of three categories — Early Blight, Late Blight, or Healthy ,along with a confidence score and actionable treatment/prevention advice.

Built as part of my MCA academic project at Integral University.

---

🎯 Problem Statement

Potato crops are highly susceptible to fungal diseases like Early Blight and Late Blight, which can spread quickly and cause major yield loss if not identified early. Farmers often don't have quick access to agricultural experts. This system provides an instant, accessible way to identify the disease from a leaf photo and get clear next steps.

---

🛠️ Tech Stack

| Component | Technology Used |

 Backend : Flask (Python) 
 Deep Learning :  TensorFlow / Keras 
 Model Architecture : CNN with MobileNetV2 (Transfer Learning) 
 Image Processing : OpenCV 
 Database : SQLite 
 Frontend : HTML, CSS, JavaScript (Jinja templates) 

---

 🧠 How It Works

1. Image Upload: User uploads a potato leaf image via the web interface
2. Leaf Validation: The image is checked using HSV color analysis (OpenCV) to confirm it actually contains significant green leaf content — invalid/irrelevant images are rejected before prediction
3. Prediction: The image is resized to 224×224 and passed through a MobileNetV2-based CNN model, which outputs a classification: Early Blight, Late Blight, or Healthy
4. Confidence Check: If the model's confidence is below 85%, the result is flagged as "Invalid/Unknown" and the user is asked to upload a clearer image
5. Recommendation: Cause, treatment, and prevention tips are displayed based on the predicted class
6. History Logging: Every prediction (filename, result, confidence, timestamp) is saved to a SQLite database
7. Admin Dashboard: A password-protected admin panel lets you view the full prediction history

---

📸 Screenshots

Landing Page
[Landing Page](screenshots/landing-page.png)

About the Project
[About Project](screenshots/about-project.png)

How It Works
[How It Works](screenshots/how-it-works.png)

Upload Page
[Upload Page](screenshots/upload-page.png)

Prediction Result — Healthy Leaf
[Healthy Result](screenshots/healthy-leaf-result.png)

Prediction Result — Late Blight Detected
[Late Blight Result](screenshots/late-blight-result.png)

---


🌟 Key Features

Transfer learning with MobileNetV2 — lightweight and efficient, suitable for low-resource deployment
Leaf validation layer — filters out non-leaf images before they reach the model, reducing false predictions
Confidence thresholding — avoids confidently wrong predictions on unclear images
Prediction history + admin dashboard — tracks usage and results over time
Simple, clean web interface — no technical knowledge needed to use it

---

 📊 Model Details

Base Model: MobileNetV2 (pre-trained on ImageNet), with a custom classification head (`GlobalAveragePooling2D → Dense(1024, ReLU) → Dense(3, Softmax)`)
Classes: Early Blight, Healthy, Late Blight
Input size: 224×224 RGB images
Training approach: Base MobileNetV2 layers frozen; only the custom head trained (fast, efficient transfer learning)
Confidence threshold: 85% — predictions below this are marked as unreliable

---

 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
pip
```

### Installation
```bash
git clone https://github.com/your-username/potato-leaf-disease-detection.git
cd potato-leaf-disease-detection
pip install -r requirements.txt
```


### Run the app
```bash
python app.py
```
Visit `http://localhost:8000` in your browser.

*(To retrain the model on your own dataset, run `python train_model.py`)*

---

📁 Project Structure
```
potato-leaf-disease-detection/
├── app.py                  # Flask application & prediction logic
├── train_model.py          # Model training script (MobileNetV2)
├── potato_model.h5         # Trained model file
├── dataset/                # Training images (Early Blight, Late Blight, Healthy)
├── templates/               # HTML templates (index, admin login, admin dashboard)
├── static/                 # CSS, JS, uploaded images
├── project.db               # SQLite database (prediction history)
└── requirements.txt
```

---

🔮 Future Improvements
- Expand to detect diseases in other crops beyond potato
- Replace hardcoded admin password with proper authentication
- Deploy on cloud (Render/Railway) for public access
- Add mobile-friendly / PWA support for in-field use
- Add multilingual treatment recommendations (Hindi, regional languages)

---

👤 Author
Built as part of my MCA coursework at Integral University.

*Feel free to connect if you'd like to discuss the project or collaborate!*
