from django.shortcuts import render

# Create your views here.
def hi(request):
    return HttpResponse("Hello")
