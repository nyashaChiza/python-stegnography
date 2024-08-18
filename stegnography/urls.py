from django.urls import path
from stegnography import views

urlpatterns = [
    path('text/encode/', views.text_encode_view, name='text_encode'),
    path('text/decode/', views.text_decode_view, name='text_decode'),
    path('file/encode/', views.file_encode_view, name='file_encode'),
    path('file/decode/', views.file_decode_view, name='file_decode'),
    path('download/<str:file_name>/', views.download_file, name='download'),
]
