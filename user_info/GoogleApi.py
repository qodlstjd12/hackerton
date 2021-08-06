import io
import os
import re
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision_v1 import types

def google_api(t_path):

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

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\duddl\\dulcet-iterator-320723-e838186e72f3.json"

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
        
    text = text.replace("\n", "")
    phoneNumRegex1 = re.compile(r'\d{3}-\d{4}-\d{4}') # ^는 문장의 시작을 의미
    phoneNumRegex2 = re.compile(r'(?P<NAME>\w+)+님') # ~님 이름 뽑는 정규표현식
    phoneRegex = re.compile(r'''(
        (\d{2}|\(\d{2}\)|\d{3}|\(\d{3}\))?      # 지역번호 : 2자리 또는 3자리, () 포함, 0번또는 1번  
        (-)?                                # 구분자 : 하이푼 또는 . 0번 또는 1번  
        (\d{3}|\d{4})                           # 3자리 또는 4자리 숫자  
        (-)                               # 구분자  
        (\d{4})                                 # 4자리 숫자  
        )''', re.VERBOSE)
 
    print(text)

    if phoneNumRegex1.findall(text) != [] :
        print("phoneNumRegex1")
        return False
    elif phoneRegex.findall(text) != [] :
        print(phoneRegex.findall(text))
        return False
    else:
       for i in area:
            print(text.find(i))
            if text.find(i) != -1:
                print("area")
                return False
    return True
        