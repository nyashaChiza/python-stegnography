from django.shortcuts import render

def encode_view(request):
    return render(request, 'stegnography/encode.html')

def decode_view(request):
    return render(request, 'stegnography/decode.html')
