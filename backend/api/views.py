from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse

def hello(request):

    return JsonResponse({'message': 'Hello from Django!'})


def api_home(request):
    return JsonResponse({'message': 'Hello from Django!'})