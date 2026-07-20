import os
import numpy as np
import sqlite3
import cv2 
import requests
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)


API_KEY = "YOUR_OPENWEATHERMAP_API_KEY" 
CITY = "Lucknow"
MODEL_PATH = 'potato_model.h5'
model = load_model(MODEL_PATH)
CLASS_NAMES = ['Early Blight', 'Healthy', 'Late Blight']
CONFIDENCE_THRESHOLD = 0.85 


DISEASE_INFO = {
    'Early Blight': {
        'cause': 'Fungus (Alternaria solani)',
        'treatment': 'Use fungicides like Mancozeb. Ensure air circulation.',
        'prevention': 'Rotate crops, avoid overhead watering.'
    },
    'Late Blight': {
        'cause': 'Oomycete (Phytophthora infestans)',
        'treatment': 'Apply Copper-based fungicides immediately. Destroy infected plants.',
        'prevention': 'Use certified seeds, monitor humidity levels.'
    },
    'Healthy': {
        'cause': 'None',
        'treatment': 'Your plant is healthy! No chemical treatment needed.',
        'prevention': 'Maintain regular watering and soil nutrition.'
    }
}

def get_lucknow_humidity():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url).json()
        return response['main']['humidity']
    except:
        return None

def is_valid_leaf(img_path):
    img = cv2.imread(img_path)
    if img is None: return False
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = np.sum(mask > 0) / (img.shape[0] * img.shape[1])
    return green_ratio > 0.05

def init_db():
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       filename TEXT, result TEXT, confidence REAL, 
                       timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    # Fix for Screenshot (4086).png: Passing empty info to avoid UndefinedError
    return render_template('index.html', info={})

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files: return "No file uploaded"
    file = request.files['file']
    if file.filename == '': return "No file selected"

    upload_folder = os.path.join('static', 'uploads')
    if not os.path.exists(upload_folder): os.makedirs(upload_folder)
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    if not is_valid_leaf(filepath):
        dummy_info = {'cause': 'N/A', 'treatment': 'Not a plant leaf detected.', 'prevention': 'N/A'}
        return render_template('index.html', prediction="Invalid Image", confidence="N/A", img_path=filepath, info=dummy_info)

    # Prediction
    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    predictions = model.predict(img_array)
    max_score = np.max(predictions)
    predicted_class = CLASS_NAMES[np.argmax(predictions)]

    humidity = get_lucknow_humidity()
    # Get info and create a copy to add weather advice
    current_info = DISEASE_INFO.get(predicted_class, {'cause':'N/A','treatment':'N/A','prevention':'N/A'}).copy()
    
    if max_score < CONFIDENCE_THRESHOLD:
        final_result = "Invalid/Unknown Image"
        current_info = {'cause': 'Unknown', 'treatment': 'Please upload a clearer potato leaf photo.', 'prevention': 'N/A'}
    else:
        final_result = predicted_class
        if humidity and humidity > 80 and predicted_class != 'Healthy':
            current_info['treatment'] += f" (Note: Lucknow Humidity is {humidity}%, apply treatment urgently!)"

    # Database Log
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (filename, result, confidence) VALUES (?, ?, ?)", 
                   (file.filename, final_result, float(max_score)))
    conn.commit()
    conn.close()

    return render_template('index.html', prediction=final_result, confidence=f"{max_score*100:.2f}%", img_path=filepath, info=current_info)

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_dashboard', methods=['POST'])
def admin_dashboard():
    password = request.form.get('password')
    if password == 'admin123':
        conn = sqlite3.connect('project.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history ORDER BY id DESC")
        data = cursor.fetchall()
        conn.close()
        return render_template('admin_dashboard.html', history=data)
    return render_template('admin_login.html', error="Wrong Password")

if __name__ == "__main__":
    init_db()
    # 0.0.0.0  for wifi network
    app.run(host='0.0.0.0', port=8000, debug=True)