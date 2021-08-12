import io
import os
import re
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision_v1 import types
from .models import UserInfo, CustomUser

def ggoo(t_path, name):

    area = [
    "강원",
    "경기",
    "충남",
    "충북",
    "전북",
    "전남",
    "경북",
    "경남",
    "제주",
    "서울",
    "인천",
    "대전",
    "울산",
    "부산",
    "대구",
    "광주",
    "세종"
    ]

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\LGPC\\Desktop\\LikeLion\\hackerton\\resources\\dulcet-iterator-320723-e838186e72f3.json"

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    # file_name = os.path.join(
    #     os.path.dirname(__file__),
    #     t_path)

    # # Loads the image into memory
    # with io.open(file_name, 'rb') as image_file:
    #     content = image_file.read()
    # print(content)
    # print(type(content))
    content = t_path
    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.text_detection(image=image)
    labels = response.text_annotations

    text = ""
    for label in labels:
        text = label.description + text
    
    if name in text:
        return True
    else:
        return False