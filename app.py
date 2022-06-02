from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
import cv2
from werkzeug.utils import secure_filename
import numpy as np
import image_similarity_measures
import face_recognition

app = Flask(__name__)


@app.route("/")             #HomePage
def uploader():
    
    path = 'static/uploads/'
    uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(
        path+x))        # Sorting as per image upload date and time
    print(uploads)
    
    uploads = ['uploads/' + file for file in uploads]
    uploads.reverse()
    
    # Pass filenames to front end for display in 'uploads' variable
    return render_template("index.html", uploads=uploads)


app.config['UPLOAD_FOLDER'] = 'static/uploads'             # Storage path


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():                                       # This method is used to upload files
    if request.method == 'POST':
        f = request.files['file']
        print(f.filename)
        
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Redirect to route '/' for displaying images on front end
        return redirect("/")


#capture image

@app.route('/static/uploads/')
def my_link():
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            
            if key == ord('s'): 
                cv2.waitKey(1000)
                print("Processing image...")

                path = '/static/uploads/'
                cv2.imwrite(os.path.join(path , 'frame.jpg'), img=frame)
                print("Processing image...")
                img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
        
            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break
        
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
            
    return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.run()