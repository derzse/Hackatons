from flask import Flask, request, send_file, render_template
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        print("Read the image in bytes and convert to a format that OpenCV understands")
        in_memory_file = io.BytesIO()
        file.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        image = cv2.imdecode(data, color_image_flag)

        # Perform edge detection
        edges = cv2.Canny(image, 100, 200)

        # Convert back to binary image
        is_success, buffer = cv2.imencode(".jpg", edges)
        if not is_success:
            return 'Error processing image', 500

        # Convert to bytes and send back as a response
        io_buf = io.BytesIO(buffer)
        return send_file(io_buf, mimetype='image/jpeg', as_attachment=True, download_name='edges.jpg')


    return 'Invalid file', 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg'}

if __name__ == '__main__':
    app.run(debug=True)
