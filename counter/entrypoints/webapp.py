import threading
from io import BytesIO
from PIL import Image

from flask import Flask, request, jsonify

from counter import config
app = Flask(__name__)


count_action = config.get_count_action()
list_action = config.get_list_action()

from counter.loggers import logging

# Maximum allowed file size (in bytes)
MAX_FILE_SIZE = 1 * 1024 * 1024  # 2 MB

def validate_threshold(threshold):
    try:
        threshold = float(threshold)
        if 0.0 <= threshold <= 1.0:
            return threshold
    except ValueError:
        pass
    return None

@app.route('/object-count', methods=['POST'])
def object_detection():
    uploaded_file = request.files.get('file')
    threshold = request.form.get('threshold', '0.5')

    if not uploaded_file:
        logging.info('No file provided')

        return jsonify({'error': 'No file provided.'}), 400

    threshold = validate_threshold(threshold)
    if threshold is None:
        logging.error('Invalid threshold value. Please provide a float value between 0.0 and 1.0.')
        
        return jsonify({'error': 'Invalid threshold value. Please provide a float value between 0.0 and 1.0.'}), 400

    if len(uploaded_file.read()) > MAX_FILE_SIZE:
        return jsonify({'error': 'File size exceeds the allowed limit.'}), 400

    uploaded_file.seek(0)
    image_data = uploaded_file.read()

    try:
        image = BytesIO(image_data)
        count_response = count_action.execute(image, threshold)

    except Exception as e:
        logging.info('Failed to process the image. Please ensure it is a valid image file')

        return jsonify({'error': 'Failed to process the image. Please ensure it is a valid image file.'}), 400
    

    return jsonify(count_response)

@app.route('/object-list', methods=['POST'])
def detected_object_list():
    uploaded_file = request.files.get('file')
    threshold = request.form.get('threshold', '0.5')

    if not uploaded_file:
        logging.info('No file provided')
 
        return jsonify({'error': 'No file provided.'}), 400

    threshold = validate_threshold(threshold)

    if threshold is None:
        logging.error('Invalid threshold value. Please provide a float value between 0.0 and 1.0.')

        return jsonify({'error': 'Invalid threshold value. Please provide a float value between 0.0 and 1.0.'}), 400

    if len(uploaded_file.read()) > MAX_FILE_SIZE:
        return jsonify({'error': 'File size exceeds the allowed limit.'}), 400

    uploaded_file.seek(0)
    image_data = uploaded_file.read()

    try:
        image = BytesIO(image_data)
        count_response = list_action.execute(image, threshold)

    except Exception as e:
        logging.info('Failed to process the image. Please ensure it is a valid image file')

        return jsonify({'error': 'Failed to process the image. Please ensure it is a valid image file.'}), 400


    return jsonify(count_response)

if __name__ == '__main__':

    app.run('0.0.0.0',debug=True)

