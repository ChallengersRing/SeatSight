from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from .detector import Detector
from django.conf import settings
from .tools import process_frame
from .tools import set_logger
from django.contrib.auth.decorators import login_required

# Initilizations
set_logger()
yolo_path = os.path.join(settings.BASE_DIR, 'utils', 'yolov3')
model_path = os.path.join(settings.BASE_DIR, 'utils', 'yolov3', 'yolov3.pt')
names_path = os.path.join(settings.BASE_DIR, 'utils', 'coco.names')
# Instantiate the model processing class
detector = Detector(yolo_path, model_path, names_path)

# Create your views here. //controllers
# these mtds called from urls.py[controller?] with param HttpRequest
# Define a view to handle the detection request
# @login_required(login_url='account/')
def index(request):
    # render mtd takes param HttpRequest,template,context and return HttpResponse
    return render(request, "index.html")

# @login_required(login_url='account/')
@csrf_exempt
def process_image(request):
    print("FROM PROCESS IMAGE:...............................................................")
    if request.method == "POST":
        # Get the image file from the request
        image_frame = request.FILES.get("image", None)
        # image_frame = request.body
        print("org image file: ",image_frame)

        # If no image is provided, return an error response
        if not image_frame:
            return JsonResponse({"error": "No image provided."}, status=400)
        
        if os.path.splitext(str(image_frame))[1].lower() not in [".jpg", ".jpeg", ".png"]:
            return JsonResponse({"error": "Input is not an image."}, status=400)
        
        response_data = process_frame(detector, image_frame, True)

        return JsonResponse(response_data, status=response_data["status"])
        
    else:
        print("method is not post")
        # If the request method is not POST, return an error response
        return JsonResponse({"error": "Invalid request method."}, status=405)
