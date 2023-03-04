import os
from django.shortcuts import render

# Create your views here.


def home(request):
    if request.method == "POST":
        file = request.FILES['file']
        #doc = Document.objects.create(session_id=request.session['user_id'], file=file)
        #doc.save()
        return True
    context = {}
    return render(request, 'home.html', context)
