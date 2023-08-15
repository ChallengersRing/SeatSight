from django.conf import settings
from PIL import Image, ExifTags
import os
import base64
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import traceback
import logging
import colorlog

def process_frame(detector, frame, isSingleFrame):
    print("FROM PROCESS FRAME:...............................................................")
    if(isSingleFrame):
        PILimage = Image.open(frame)
        width, height = PILimage.size
        print(width,height)
        
        # Convert the image to 640*640
        if (width>640 or height >640):
            PILimage = image_converter(PILimage, (640, 640))

        # image_bytes = frame.read()
        # Convert the image to bytes
        buffer = BytesIO()
        PILimage.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()
        image_np = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    else:
        image = frame

    try:
        # Detect objects in the image
        img, data = detector.predict(image)

        # Encode the image as a base64 string
        retval, encoded_image = cv2.imencode('.jpeg', img)
        base64_image = base64.b64encode(encoded_image).decode('utf-8')

        # Create a dictionary with the data and image
        response_data = {
            "data": data,
            "image": base64_image,
            "status": 200            
        }
        return response_data
    
    except Exception as e:
        traceback.print_exc()
        response_data = {
            "data": str(e),
            "image": None,
            "status": 500            
        }
        return response_data
    
def image_converter(original_image, dimension):
    # Get the EXIF data from the image
    try:
        exif_data = original_image._getexif()
    except AttributeError:
        exif_data = None

    # Rotate the image according to the EXIF orientation data
    if exif_data is not None:
        for tag, value in exif_data.items():
            if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == 'Orientation':
                if value == 3:
                    original_image = original_image.rotate(180, expand=True)
                elif value == 6:
                    original_image = original_image.rotate(270, expand=True)
                elif value == 8:
                    original_image = original_image.rotate(90, expand=True)
                break
            
    # Resize the image while maintaining aspect ratio
    original_image.thumbnail(dimension)

    # Create a new blank image with the target size
    converted_image = Image.new("RGB", dimension)

    # Paste the resized image onto the new image
    x_offset = (dimension[0] - original_image.size[0]) // 2
    y_offset = (dimension[1] - original_image.size[1]) // 2
    converted_image.paste(original_image, (x_offset, y_offset))

    return converted_image


# Create a logger
logger = logging.getLogger()
def set_logger():
    logger.setLevel(logging.INFO)
    # Create a file handler and set its log level
    log_path = os.path.join(settings.BASE_DIR, 'utils', 'log_file.log')
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    # Add the file handler to the logger
    logger.addHandler(file_handler)
    # Create a colored formatter
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'
        })
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # Add the console handler to the logger
    logger.addHandler(console_handler)

def get_logger():
    return logger