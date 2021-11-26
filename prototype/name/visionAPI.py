import os, io
from pathlib import Path

from google.cloud import vision
from gtts import gTTS

BASE_DIR = Path(__file__).resolve().parent.parent

env_list = dict()

local_env = open(os.path.join(BASE_DIR, '.env'))

while True:
    line = local_env.readline()
    if not line:
        break
    line = line.replace('\n', '')
    start = line.find('=')
    key = line[:start]
    value = line[start+1:]
    env_list[key] = value

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_list['GOOGLE_API_KEY']


def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    text_list = []
    for text in texts:
        text_list.append(text.description)

    tts_2 = gTTS(text=text_list[0], lang='ko')
    tts_2.save("media/text.mp3")

    return text_list[0]
