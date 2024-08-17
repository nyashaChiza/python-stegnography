from django.urls import path
from stegnography import views

urlpatterns = [
    path('encode/', views.encode_view, name='encode'),
    path('decode/', views.decode_view, name='decode'),
]
