from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse

from .predict import predict_image
from .visionAPI import detect_text
from gtts import gTTS

# Create your views here.


# 메인화면
def index(request):
    intro = "너의 이름은 서비스가 실행되었습니다.\
             화면을 터치하시면 사진 촬영 페이지로 넘어갑니다."

    tts_intro = gTTS(text=intro, lang='ko')
    tts_intro.save("media/intro.mp3")

    tts_intro = settings.MEDIA_URL + "intro.mp3"
    context = {'tts_intro': tts_intro}

    return render(request, 'name/main.html', context)

# 이미지 업로드
def upload(request):
    upload_info = "상품 인식을 위해 화면을 터치해 주세요."

    tts_upload = gTTS(text=upload_info, lang='ko')
    tts_upload.save("media/upload_info.mp3")

    tts_upload = settings.MEDIA_URL + "upload_info.mp3"
    context = {'tts_upload': tts_upload}

    return render(request, 'name/upload.html', context)

# 이미지처리 결과
def result_img(request):
    img_info = "상품명을 다시 들으시려면 화면 상단을 터치해 주세요.\
                상품에 있는 텍스트를 확인하시려면 화면 하단을 터치해 주세요."

    tts_img = gTTS(text=img_info, lang='ko')
    tts_img.save("media/img_info.mp3")

    tts_img = settings.MEDIA_URL + "img_info.mp3"

    uploaded_file = request.FILES['img_uploaded']
    fs = FileSystemStorage()
    uploaded_filename = fs.save(uploaded_file.name, uploaded_file)
    uploaded_file_url = fs.url(uploaded_filename)

    pred_result = predict_image("." + uploaded_file_url)

    result_name = pred_result[0]
    result_value = pred_result[1]
    rank = pred_result[2]
    rank_value = pred_result[3]

    tts = settings.MEDIA_URL + "result.mp3"

    context = {
        'uploaded_file_url': uploaded_file_url,
        'uploaded_file_name': uploaded_filename,
        'result_name': result_name,
        'result_value': round(result_value*100, 2),
        'rank': rank,
        'rank_value': rank_value,
        'tts': tts,
        'tts_img': tts_img
        }

    return render(request, 'name/result_img.html', context)

# vision API 텍스트 처리 결과
def result_text(request, file_name):
    text_info = "다시 들으시려면 화면 상단을 터치해 주세요.\
                 처음으로 돌아가시려면 화면 하단을 터치해 주세요."

    tts_text = gTTS(text=text_info, lang='ko')
    tts_text.save("media/text_info.mp3")

    tts_text = settings.MEDIA_URL + "text_info.mp3"

    try:
        detected_text = detect_text("." + settings.MEDIA_URL + file_name)
    except IndexError:
        return HttpResponseRedirect(reverse('name:text_error'))

    tts_2 = settings.MEDIA_URL + "text.mp3"

    context = {'uploaded_file_url': settings.MEDIA_URL+file_name,
               'uploaded_file_name': file_name,
               'text_list': detected_text,
               'tts_2': tts_2,
               'tts_text': tts_text
               }

    return render(request, 'name/result_text.html', context)

def text_error(request):
    text_error_info = "텍스트를 읽을 수 없습니다.\
                       화면을 터치하시면 사진 촬영 페이지로 넘어갑니다."

    tts_text_error = gTTS(text=text_error_info, lang='ko')
    tts_text_error.save("media/text_error_info.mp3")

    tts_text_error = settings.MEDIA_URL + "text_error_info.mp3"
    context = {'tts_text_error': tts_text_error}

    return render(request, 'name/text_error.html', context)