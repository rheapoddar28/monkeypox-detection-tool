import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
#from covid import run_model

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./templates/index.html')

@app.route('/predict', methods = ['GET', 'POST'])
def upload ():
    if request.method == 'POST':

        f = request.files['file']

        base_path = os.path.dirname(__file__)
        file_path = os.path.join(basepath, "uploads", secure_filename(f.filename))
        f.save(file_path)
        print(file_path)
    return None



if __name__ == '__main__':
    app.run()
