from django.shortcuts import render
from accounts.models import Profile
from .models import Leave
from PyPDF2 import PdfReader
from fuzzywuzzy import fuzz
import nltk
import re
import pickle
import os

parameters = {
    "age": None,
    "bmi": None,
    "systolicBloodPressure": None,
    "diastolicBloodPressure": None,
    "bloodGlucose": None,
    "temperature": None,
    "chronicHypertension": None,
    "familyHistory": None,
    "placentaAbruption": None,
    "pretermLabour": None,
    "multipleGestation": None
}

parametersusingNLTK = {
    "age": None,
    "bmi": None,
    "systolicBP": None,
    "diastolicBP": None,
    "bloodGlucose": None,
    "temperature": None,
    "chronicHypertension": None,
    "familyHistory": None,
    "placentaAbruption": None,
    "pretermLabour": None,
    "multipleGestation": None
}

# Create your views here.
def uploadPDF(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user.id)
        report = request.FILES['pdf']
        date = request.POST['pregnant']
        try:
            os.remove('media/report.pdf')
        except:
            pass
        leave = Leave.objects.create(profile=profile, report=report, pregnancy_date=date)
        leave.save()
        os.rename(('media/'+report.name).replace(" ", "_"), 'media/report.pdf')
        readPDF(request, leave)
    try:
        user_leave = Leave.objects.get(profile=(Profile.objects.get(user=request.user)))
        status = user_leave.leave_approved
    except:
        status = None
    context = {"status": status}
    return render(request, "leave.html", context)

def readPDF(request, leave):
    reader = PdfReader('media/report.pdf')
    text = ""
    for pageNo in range(len(reader.pages)):
        page = reader.pages[pageNo]
        text += page.extract_text()
    extractData(request, text)
    predictMaternalRisk(leave)
    return None

def extractData(request, text):
    text = text.split('\n')
    for counter in range(len(text)):
        text[counter] = text[counter].strip()
        text[counter] = [text[counter][:text[counter].rfind(' ')].strip(), text[counter][text[counter].rfind(' ')+1:].strip()]
    for line in text:
        for parameter in parameters.keys():
            if "Years" in line[1]:
                parameters["age"] = line[1].replace("Years", '') 
            fuzzy_index = fuzz.token_sort_ratio(line[0].lower().replace(' ', ''), parameter.lower())
            if fuzzy_index > 90:
                parameters[parameter] = line[1]
    return

def extractDataUsingNLTK(request, text):
    text = removeParenthesis(request, text)
    text = removespecialCharacters(request, text)
    tokenized = nltk.word_tokenize(text)
    for counter in range(len(tokenized)-1):
        for parameter in parameters.keys():
            fuzzy_index = fuzz.token_sort_ratio(tokenized[counter].lower(), parameter.lower())
            if fuzzy_index > 90:
                parameters[parameter] = tokenized[counter+1]
    return

def removeParenthesis(request, text):
    i = 0
    while(any([bracket in text for bracket in ['(', ')', '[', ']']]) and i<10):
        # Removing the data enclosed within ()
        re.sub(r"\s?[\[].*?[\]]", "", text)
        # Removing the data enclosed within []
        re.sub(r"\s?[\()].*?[\)]", "", text)
        i += 1
    text.replace("(", "")
    text.replace(")", "")
    text.replace("[", "")
    text.replace("]", "")
    return text

def removespecialCharacters(request, text):
    pattern = r'[^a-zA-Z0-9\s]'
    text = re.sub(pattern, '', text)
    return text

def predictMaternalRisk(leave):
    pickled_model = pickle.load(open('leaveCalculator/classifier.pkl', 'rb'))
    ch = 0
    fh = 0
    pa = 0
    pl = 0
    mg = 0
    if parameters["chronicHypertension"] == 'Positive':
        ch = 1
    else:
        ch = 0
    if parameters["familyHistory"] == "Yes":
        fh = 1
    else:
        fh = 0
    if parameters["placentaAbruption"] == "Yes":
        pa = 1
    else:
        pa = 0
    if parameters["pretermLabour"] == "Yes":
        pl = 1
    else:
        pl = 0
    if parameters["multipleGestation"] == "Yes":
        mg = 1
    else:
        mg = 0
    age = int(parameters["age"])
    bmi = int(parameters["bmi"])
    systolicBP = float(parameters["systolicBloodPressure"])
    diastolicBP = float(parameters["diastolicBloodPressure"])
    bloodGlucose = float(parameters["bloodGlucose"])
    bodyTemp = float(parameters["temperature"])
    list = pickled_model.predict([[age, bmi, systolicBP, diastolicBP, bloodGlucose, bodyTemp, ch, fh, pa, pl, mg]])
    if list[0] == 0:
        leave.maternity_leave += 1
    elif list[0] == 1:
        leave.maternity_leave += 2
    else:
        leave.maternity_leave += 3
    leave.save()
    return None

def leavedash(request):
    leaves = list(Leave.objects.filter(leave_approved = False))
    context = {'leaves': leaves}
    return render(request, "hr_dashboard.html", context)

def leaveprofile(request, the_slug):
    leave = Leave.objects.get(slug=the_slug)
    if request.method=="POST":
        approval = request.POST['approval']
        if approval == "Accept":
            leave.leave_approved = True
            leave.save()
            print(leave.leave_approved)
    context = {"leave": leave}
    return render(request, "leaveprofile.html", context)
