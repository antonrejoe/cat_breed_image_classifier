from flask import Flask, render_template, request, redirect, url_for
# if you encounter dependency issues using 'pip install flask-uploads'
# try 'pip install Flask-Reuploaded'
from flask_uploads import UploadSet, configure_uploads, IMAGES
from keras.preprocessing.image import load_img
# the pretrained model
from model import predict_class

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

# path for saving uploaded images
app.config['UPLOADED_PHOTOS_DEST'] = './static/img'
configure_uploads(app, photos)

# professionals have standards :p
@app.route('/home', methods=['GET', 'POST'])
def home():
    welcome = "Hello, World !"
    return welcome

# the main route for upload and prediction
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        # save the image
        filename = photos.save(request.files['photo'])
        # load the image
        image = './static/img/' + filename 
        # make prediction
        label, probability = predict_class(image)
        # Redirect to the result page with the prediction results
        # return redirect(url_for('result', label=label, probability=probability, filename=filename))
        return {"result": label , "probability": probability }
    # web page to show before the POST request containing the image
    return render_template('upload.html')

    

@app.route('/result')
def result():
    label = request.args.get('label')
    probability = request.args.get('probability')
    filename = request.args.get('filename')

    if not label or not probability or not filename:
        return redirect(url_for('upload'))

    return render_template('result.html', label=label, probability=probability, filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
