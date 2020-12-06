# try:
#     import unzip_requirements
# except ImportError:
#     pass

import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import requests

#import boto3
from google.cloud import storage

import os
import io
import json
import base64
from requests_toolbelt.multipart import decoder
print("Import End...")


# Define Env Variables
GCS_BUCKET = os.environ['GCS_BUCKET'] if 'GCS_BUCKET' in os.environ else 'sls-dev0099'
MODEL_PATH = os.environ['MODEL_PATH'] if 'MODEL_PATH' in os.environ else 'mobilenetV2.pt'
LABELS_PATH=os.environ['LABELS_PATH'] if 'LABELS_PATH' in os.environ else 'imagenet_labels.json'

print("Downloading Model...")

client = storage.Client()
bucket = client.get_bucket(GCS_BUCKET)

try:
    blob = bucket.get_blob(MODEL_PATH)
    print("Loading Blob..")
    blob.download_to_filename('/tmp/mobilenetV2.pt')
    # print("Creating Bytestream...")
    # bytestream = io.BytesIO(blob)
    print("Loading Model")
    model = torch.jit.load('/tmp/mobilenetV2.pt', map_location = torch.device('cpu'))
    print("Model Loaded...")
    

    blob = bucket.blob(LABELS_PATH)
    print('Loading Labels')
    labels = json.loads(blob.download_as_string(client=None))
    print('Labels loaded')
    
except Exception as e:
    print(repr(e))
    raise(e)


def transform_image(image_bytes):
    try:
        transformations = transforms.Compose([
            transforms.Resize(255),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
        # image = Image.open(io.BytesIO(image_bytes))
        image = Image.open(image_bytes).convert('RGB')
        print('image read')
        return transformations(image).unsqueeze(0)
    except Exception as e:
        print(repr(e))
        raise(e)

def get_prediction(image_bytes):
    print('get_prediction called')
    tensor = transform_image(image_bytes=image_bytes)
    return model(tensor).argmax().item()



def classify_image(event):
    try:
        print(event)
        print(event.files.to_dict())
        print(list(event.files.to_dict().values())[0])
        # inFile = list(event.files.to_dict().values())[0]
        # body = base64.b64decode(inFile)
        fileobj = event.files['']

        print(fileobj)
        print("BODY LOADED...")

        # picture = decoder.MultipartDecoder(body, content_type_header).parts[0]
        prediction = get_prediction(image_bytes = fileobj)
        label = labels[str(prediction)]

        print(prediction,label)

        # filename = picture.headers[b'Content-Disposition'].decode().split(';')[1].split('=')[1]
        # if len(filename) < 4:
        #     filename = picture.headers[b'Content-Disposition'].decode().split(';')[2].split('=')[1]
        # print('filename: '+filename.replace('"',''))

        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({'predicted': prediction, 'label': label})
        }
        
    
    except Exception as e:
        print(repr(e))
        return {
            "statuscode" : 500,
            "headers" : {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin' : '*',
                'Access-Control-Allow-Credentials' : True
            },
            "body": json.dumps({"error": repr(e)})
        }