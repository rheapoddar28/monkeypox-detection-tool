import os
from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import tensorflow as tf
from matplotlib.pyplot import imread
from matplotlib.pyplot import imshow
from keras.preprocessing import image
from keras.utils import img_to_array, load_img
from math import ceil
import cv2
from io import BytesIO
#"/Users/rhesaurus/monkeypox-detection-tool/VGG-16 modified/vgg_16_finetune.weights.best.hdf5"


app = Flask(__name__)

# Replace 'path_to_model' with the actual path to your trained model file
MODEL_PATH = "/Users/rhesaurus/monkeypox-detection-tool/VGG-16 modified/vgg_16_finetune.weights.best.hdf5"
model = tf.keras.models.load_model(MODEL_PATH)

# Define the class labels for the model
CLASSES = ['Normal', 'Monkeypox', 'Measles', 'Chickenpox']

# ... Rest of the code, including the 'allowed_file' function ...
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/worldwidecases')
def worldwidecases():
    return render_template('/worldwide-cases.html')

@app.route('/aboutmonkeypox')
def aboutmonkeypox():
    return render_template('/about-monkeypox.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        # If the user does not select a file, the browser may send an empty file
        if file.filename == '':
            return "No selected file"
        
        if file and allowed_file(file.filename):
            # Read the image from the request directly into memory
            image = Image.open(file)
            image_np = img_to_array(image)
            image_np = cv2.resize(image_np, (224, 224))
            image_np = np.expand_dims(image_np, axis=0)
            #image_np = preprocess_input(image_np)


            # Preprocess the image (resize, normalize, etc.) to match the input requirements of your model
            
            #processed_image = processed_image / 255.0  # Normalize pixel values to [0, 1]
            #processed_image = np.expand_dims(processed_image, axis=0)

            # Make predictions using the model
            predictions = model.predict(image_np)

            # Get the probability for the class 'Monkeypox' (assuming it's the fourth class in the list)
            monkeypox_probability = 100*(predictions[0][1])

            # Save the uploaded image to a BytesIO object
            img_io = BytesIO()
            image.save(img_io, 'JPEG')
            img_io.seek(0)

            # Generate a URL for the uploaded image
            image_url = url_for('uploaded_file', filename=secure_filename(file.filename))

            return render_template('index.html', prediction=monkeypox_probability)


# Set the UPLOAD_FOLDER to 'static/uploads'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def save_uploaded_file(file):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
