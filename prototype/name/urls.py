from django.urls import path

from name import views
from name.views import index

app_name = 'name'

urlpatterns = [
    path('', index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('result_img/', views.result_img, name='result_img'),
    path('result_text/<str:file_name>', views.result_text, name='result_text'),
    path('text_error/', views.text_error, name='text_error')
]