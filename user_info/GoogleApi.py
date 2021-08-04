import io
import os
import re
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision_v1 import types

def google_api(t_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\LGPC\\Desktop\\LikeLion\\hackerton\\dulcet-iterator-320723-e838186e72f3.json"

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        t_path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.text_detection(image=image)
    labels = response.text_annotations

    text = ""
    for label in labels:
        text = label.description + text
    
    phoneNumRegex1 = re.compile(r'\d{3}-\d{4}-\d{4}') # ^는 문장의 시작을 의미
    phoneNumRegex2 = re.compile(r'(?P<NAME>\w+)+님') # ~님 이름 뽑는 정규표현식
    phoneRegex = re.compile(r'''(
        (\d{2}|\(\d{2}\)|\d{3}|\(\d{3}\))?      # 지역번호 : 2자리 또는 3자리, () 포함, 0번또는 1번  
        (|-|\.)?                                # 구분자 : 하이푼 또는 . 0번 또는 1번  
        (\d{3}|\d{4})                           # 3자리 또는 4자리 숫자  
        (\s|-|\.)                               # 구분자  
        (\d{4})                                 # 4자리 숫자  
        )''', re.VERBOSE)
    area = [
    "강원도",
    "경기도",
    "충청남도",
    "충청북도",
    "전라북도",
    "전라남도",
    "경상북도",
    "경상남도",
    "제주특별자치도",
    "서울특별시",
    "인천광역시",
    "대전광역시",
    "울산광역시",
    "부산광역시",
    "대구광역시",
    "광주광역시",
    "세종특별자치시"
    ]
    if phoneNumRegex1.findall(text) != [] :
        return False
    elif phoneNumRegex2.findall(text) != [] :
        return False
    elif phoneRegex.findall(text) != [] :
        return False
    elif text in area:
        return False
    else:
        return True