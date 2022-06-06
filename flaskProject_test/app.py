from flask import Flask, request, jsonify
from torch_utils import transform_image, get_prediciton
app = Flask(__name__)


# @app.route('/')
# def hello_world():  # put application's code here
#     return jsonify({'sucess':'오 왔다'})

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({'error': 'no file'})
        if not allowed_file(file.filename):
            return jsonify(({'error': 'format not supported'}))

    try:
        img_bytes = file.read()
        tensor = transform_image(img_bytes)
        prediction = get_prediciton(tensor)
        data = {'prediction': prediction.item(), 'class_name': str(prediction.item())}
        return jsonify(data)

    except:
        return jsonify({'error': 'error during prediction'})

if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    app.run()
