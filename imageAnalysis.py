import base64
import io
import requests
import os

# from PIL import Image
from io import BytesIO

from google.cloud import vision_v1p3beta1 as vision
from google.cloud.vision import types
#mjhoi
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = #JSON File of the google vision api key (Obviously wouldn't put it on a public repo, I'm not dumb lol)

def img_hashtags(url):
    client = vision.ImageAnnotatorClient()
    img=requests.get(url).content
    image=vision.types.Image(content=img)
    response=client.label_detection(image=image)
    labels=response.label_annotations

    web_entity_response=client.web_detection(image=image)
    web_entity=web_entity_response.web_detection


    hashtag_string=''
    if web_entity.web_entities:
        for label in web_entity.web_entities:
            hashtag=label.description
            hashtag_baby=''
            for i in hashtag:
                if i!=' ':
                    hashtag_baby+=i
            hashtag_string+='#'+hashtag_baby+' '
    for hashtag_label in labels:
        hashtag=hashtag_label.description
        hashtag_baby=''
        for i in hashtag:
            if i!=' ':
                hashtag_baby+=i
        hashtag_string+='#'+hashtag_baby+' '



    return hashtag_string
