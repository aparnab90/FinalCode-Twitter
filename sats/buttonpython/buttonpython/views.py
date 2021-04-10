from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import requests
from subprocess import run, PIPE
import sys

@login_required
def home(request):
    return render(request, "/home/sats/buttonpython/templates/registration/success.html", {})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, '/home/sats/buttonpython/templates/registration/register.html', {'form': form})

def output(request):
    data = requests.get("https://aparnab90.github.io/sentiment-analysis/")
    print(data.text)
    data = data.text
    return render(request, 'home.html', {'data': data})


def button(request):
    return render(request, 'home.html')

def external(request):

    inp = request.POST.get('param')

    out = run([sys.executable,'/home/sats/DataExtractionTwitter.py',inp],shell=False,stdout=PIPE)

    return render(request,'/home/sats/buttonpython/templates/registration/success.html',{'data1':out.stdout, 'flag':True})
