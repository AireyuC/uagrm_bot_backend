from django.shortcuts import render

def chat_demo(request):
    return render(request, 'chat_demo.html')
